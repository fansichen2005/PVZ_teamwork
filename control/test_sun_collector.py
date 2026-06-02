# -*- coding: utf-8 -*-
"""
阳光收集器测试程序
模拟视觉识别程序更新 pvz_data.json，测试阳光自动收集功能
"""

import sys
import os
import json
import time
import random
from pathlib import Path

# 修复 Windows 终端编码问题
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def generate_test_data(sun_count):
    """
    生成测试用的游戏数据

    Args:
        sun_count: 要生成的阳光数量
    """
    # 模拟游戏界面坐标范围（根据实际游戏调整）
    x_range = (200, 1200)
    y_range = (150, 800)

    falling_sun = []
    for _ in range(sun_count):
        falling_sun.append({
            "x": random.randint(*x_range),
            "y": random.randint(*y_range)
        })

    data = {
        "sunlight": random.randint(50, 500),
        "plants": [
            {"type": "sunflower", "row": 1, "col": 1},
            {"type": "peashooter", "row": 2, "col": 3}
        ],
        "zombie": [
            {"type": "zombie", "row": 2, "col": 7}
        ],
        "falling_sun": falling_sun
    }

    return data


def write_json(filepath, data):
    """写入 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def run_simulation():
    """
    模拟视觉识别程序持续更新 pvz_data.json

    测试流程：
    1. 每 2-4 秒生成随机数量的阳光坐标
    2. 写入 pvz_data.json
    3. 观察阳光收集器是否自动点击
    """
    json_path = Path(__file__).parent.parent / "pvz_data.json"

    print("=" * 60)
    print("  阳光收集器测试程序")
    print("=" * 60)
    print(f"\n将持续更新文件: {json_path.absolute()}")
    print("请先运行: python control/auto_collect_sun.py")
    print("\n倒计时 5 秒后开始生成测试数据...")

    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)

    print("\n开始生成阳光数据（按 Ctrl+C 停止）\n")

    round_num = 1
    try:
        while True:
            # 随机生成 0-5 个阳光
            sun_count = random.randint(0, 5)
            data = generate_test_data(sun_count)

            write_json(json_path, data)

            print(f"[第 {round_num} 轮] 生成了 {sun_count} 个阳光")

            round_num += 1
            time.sleep(random.uniform(2.0, 4.0))

    except KeyboardInterrupt:
        print("\n\n测试已停止")
        print("=" * 60)


if __name__ == "__main__":
    run_simulation()
