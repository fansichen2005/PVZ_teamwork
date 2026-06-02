# -*- coding: utf-8 -*-
"""
LLM 指令模拟测试程序
模拟 LLM 输出的游戏指令，通过 GameExecutor 在画图软件中演示完整执行流程
"""

import sys
import os
import time
import subprocess
import pyautogui

# 修复 Windows 终端编码问题
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))
from executor import GameExecutor


# ── 模拟 LLM 输出的指令序列 ──────────────────────────────────────────────────
# 这是 LLM 根据游戏状态分析后输出的一轮决策，格式与 GameExecutor.execute() 一致
# 额外的 "reason" 字段是 LLM 的推理说明（不传给执行器，仅用于显示）
SIMULATED_LLM_ACTIONS = [
    {
        "action": "plant",
        "plant": "sunflower",
        "row": 0, "col": 0,
        "reason": "左上角种向日葵，优先建立阳光来源"
    },
    {
        "action": "plant",
        "plant": "sunflower",
        "row": 2, "col": 0,
        "reason": "中路再种向日葵，阳光产出翻倍"
    },
    {
        "action": "collect_sun",
        "x": 920, "y": 650,
        "reason": "收集画面中央掉落的阳光（50阳光）"
    },
    {
        "action": "plant",
        "plant": "peashooter",
        "row": 0, "col": 2,
        "reason": "第1行第3格部署豌豆射手，攻击上路僵尸"
    },
    {
        "action": "plant",
        "plant": "peashooter",
        "row": 4, "col": 2,
        "reason": "第5行第3格部署豌豆射手，攻击下路僵尸"
    },
    {
        "action": "plant",
        "plant": "wallnut",
        "row": 2, "col": 6,
        "reason": "中路第7格放坚果墙，拦截僵尸推进"
    },
    {
        "action": "collect_sun",
        "x": 1150, "y": 780,
        "reason": "收集右侧掉落阳光（25阳光）"
    },
    {
        "action": "remove",
        "row": 0, "col": 0,
        "reason": "铲掉左上向日葵，为更强植物腾位"
    },
    {
        "action": "plant",
        "plant": "repeater",
        "row": 0, "col": 0,
        "reason": "升级为双重射手，强化上路火力"
    },
    {
        "action": "plant",
        "plant": "cherry_bomb",
        "row": 2, "col": 8,
        "reason": "最右列僵尸密集，投放樱桃炸弹清场"
    },
]

# 植物名称 → 卡槽索引映射（模拟本局选择的5张卡）
PLANT_MAPPING = {
    "sunflower":   0,
    "peashooter":  1,
    "wallnut":     2,
    "repeater":    3,
    "cherry_bomb": 4,
}

# ── 画图软件画布坐标（由 show_mouse_position.py 测量得到）─────────────────────
# 画布左上角: (728, 456)，画布尺寸: 771 x 907 px
CANVAS_X0 = 728
CANVAS_Y0 = 456


def display_command(index, total, action):
    """在终端中显示当前正在处理的 LLM 指令"""
    bar = "═" * 58
    print(f"\n{bar}")
    print(f"  ▶  LLM 指令  [{index} / {total}]")
    print(f"{'─' * 58}")

    atype = action.get("action")
    if atype == "plant":
        print(f"  动作 : 种植植物")
        print(f"  植物 : {action.get('plant')}")
        print(f"  位置 : 第 {action.get('row') + 1} 行，第 {action.get('col') + 1} 列")
    elif atype == "remove":
        print(f"  动作 : 铲除植物")
        print(f"  位置 : 第 {action.get('row') + 1} 行，第 {action.get('col') + 1} 列")
    elif atype == "collect_sun":
        print(f"  动作 : 收集阳光")
        print(f"  坐标 : ({action.get('x')}, {action.get('y')})")

    if "reason" in action:
        print(f"  理由 : {action['reason']}")
    print(bar)


def build_paint_executor():
    """
    构建坐标适配画图软件的执行器。
    将游戏网格（5行×9列）和卡槽映射到画图画布区域内，
    让每次点击都落在画布上，形成可见的标记点。
    """
    executor = GameExecutor()

    # 卡槽 → 画布顶部一行（5个槽，间距110px）
    executor.SLOT_START_X = CANVAS_X0 + 40    # 768
    executor.SLOT_START_Y = CANVAS_Y0 + 24    # 480
    executor.SLOT_SPACING = 110

    # 游戏网格 → 画布主体（5行×9列，每格75×130px）
    executor.GRID_START_X = CANVAS_X0 + 40    # 768
    executor.GRID_START_Y = CANVAS_Y0 + 74    # 530
    executor.CELL_WIDTH   = 75
    executor.CELL_HEIGHT  = 130

    # 铲子 → 画布外右上侧（不影响画布内容）
    executor.SHOVEL_X = CANVAS_X0 + 730       # 1458，画布最右侧外
    executor.SHOVEL_Y = CANVAS_Y0 + 24        # 480

    executor.CLICK_DELAY = 0.25
    executor.set_plant_mapping(PLANT_MAPPING)
    return executor


def open_paint_and_prepare():
    """打开画图软件并选好画笔工具"""
    print("正在打开画图软件...")
    subprocess.Popen("mspaint")
    time.sleep(3)

    print("请将画图窗口最大化！倒计时 5 秒后开始执行...")
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)

    # 选择画笔工具（快捷键 P）
    pyautogui.press("p")
    time.sleep(0.5)
    print("画笔工具已选择\n")


def run_simulation():
    pyautogui.FAILSAFE = True   # 鼠标移到屏幕左上角可紧急中断

    print("=" * 58)
    print("  植物大战僵尸 — LLM 指令模拟测试")
    print("  提示：将鼠标移至屏幕左上角可紧急中断")
    print("=" * 58)

    open_paint_and_prepare()

    executor = build_paint_executor()
    total = len(SIMULATED_LLM_ACTIONS)
    print(f"共 {total} 条 LLM 指令，开始逐条执行...\n")

    success = 0
    for i, action in enumerate(SIMULATED_LLM_ACTIONS, 1):
        display_command(i, total, action)

        # 显示指令后暂停，让用户看清再执行
        time.sleep(0.8)

        # 执行时去掉 reason 字段，executor 不认识它
        exec_action = {k: v for k, v in action.items() if k != "reason"}
        try:
            executor.execute([exec_action])
            print(f"  ✓ 执行完成")
            success += 1
        except ValueError as e:
            print(f"  ✗ 执行失败: {e}")

        time.sleep(0.4)

    print("\n" + "=" * 58)
    print(f"  执行完毕：{success}/{total} 条指令成功")
    print("=" * 58)


if __name__ == "__main__":
    run_simulation()
