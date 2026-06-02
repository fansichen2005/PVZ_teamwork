# 植物大战僵尸 LLM 自动化项目开发日志

## 项目概述

本项目旨在借助 LLM 自动玩植物大战僵尸游戏。项目分工中，当前负责的工作是：
- 将 LLM 输出的高层次指令转换为低层次的鼠标操作
- 实现鼠标点击植物卡槽、点击铲子、点击游戏网格等功能

## 开发日期

2026年5月27日

## 技术栈

- Python 3.x
- pyautogui - 用于鼠标控制和自动化操作

## 项目结构

```
PvZ Master/
├── control/
│   ├── executor.py          # 游戏执行器主文件
│   ├── test_mouse.py        # 鼠标功能测试程序
│   └── show_mouse_position.py  # 鼠标坐标显示工具
└── PROJECT_LOG.md           # 项目开发日志（本文件）
```

## 已完成的工作

### 1. 游戏执行器 (executor.py)

创建了 `GameExecutor` 类，负责将 LLM 输出的指令转换为鼠标操作。

#### LLM 指令格式

```python
actions = [
    {
        "action": "plant",
        "plant": "peashooter",
        "row": 2,
        "col": 5
    },
    {
        "action": "remove",
        "row": 1,
        "col": 3
    },
    {
        "action": "collect_sun",
        "x": 300,
        "y": 400
    }
]
```

#### 核心功能

- `click_slot(slot)` - 点击指定的卡槽（索引从0开始）
- `click_cell(row, col)` - 点击指定行列的游戏网格
- `click_shovel()` - 点击铲子
- `collect_sun(x, y)` - 收集阳光
- `plant(plant, row, col)` - 种植植物（自动点击卡槽+网格）
- `remove_plant(row, col)` - 移除植物（自动点击铲子+网格）
- `execute(actions)` - 批量执行 LLM 输出的指令列表

#### 可配置的坐标常量

```python
# 卡槽配置
SLOT_START_X = 100      # 第一个卡槽的X坐标
SLOT_START_Y = 50       # 卡槽的Y坐标
SLOT_SPACING = 60       # 卡槽之间的间距

# 游戏网格配置
GRID_START_X = 250      # 第一列的X坐标
GRID_START_Y = 150      # 第一行的Y坐标
CELL_WIDTH = 80         # 每格的宽度
CELL_HEIGHT = 100       # 每格的高度

# 铲子位置
SHOVEL_X = 600
SHOVEL_Y = 50

# 点击延迟
CLICK_DELAY = 0.1       # 秒
```

**注意：** 这些坐标需要在实际游戏中测量并调整。

#### 使用示例

```python
# 初始化执行器
executor = GameExecutor()

# 设置植物名称到卡槽索引的映射（游戏开始时手动配置）
executor.set_plant_mapping({
    "peashooter": 0,
    "sunflower": 1,
    "wallnut": 2,
    "cherrybomb": 3,
    "repeater": 4
})

# 执行 LLM 输出的指令
actions = [
    {"action": "plant", "plant": "peashooter", "row": 2, "col": 5},
    {"action": "plant", "plant": "sunflower", "row": 1, "col": 2},
    {"action": "remove", "row": 1, "col": 3}
]
executor.execute(actions)
```

### 2. 鼠标坐标显示工具 (show_mouse_position.py)

创建了一个实时显示鼠标坐标的工具，用于测量游戏界面的关键位置。

#### 使用方法

```bash
python control/show_mouse_position.py
```

运行后会实时显示鼠标的 X 和 Y 坐标，按 Ctrl+C 退出。

#### 用途

- 测量卡槽位置
- 测量游戏网格位置
- 测量铲子位置
- 测量其他游戏界面元素的位置

### 3. 鼠标功能测试程序 (test_mouse.py)

创建了一个完整的鼠标控制测试程序，用于验证鼠标操作的准确性。

#### 测试内容

1. **绘制正方形** - 测试连续拖拽绘制
2. **绘制圆形** - 测试复杂路径绘制
3. **绘制直线** - 测试基本拖拽
4. **绘制锯齿形** - 测试多段连续绘制
5. **绘制网格** - 模拟游戏网格布局
6. **点击模式测试** - 模拟游戏中的卡槽和网格点击

#### 使用方法

```bash
python control/test_mouse.py
```

#### 程序流程

1. 3秒倒计时准备
2. 自动打开 Windows 画图软件
3. 等待5秒让用户手动最大化窗口
4. 自动按 'p' 键选择画笔工具
5. 在画布上依次绘制各种测试图形
6. 执行点击模式测试

#### 画图软件画布坐标（已测量）

通过 `show_mouse_position.py` 测量得到的画布区域：

- **画布左上角：** (728, 456)
- **画布右下角：** (1499, 1363)
- **画布尺寸：** 771 x 907 像素

这些坐标已经硬编码到 `test_mouse.py` 中，确保绘图在正确的画布区域内进行。

#### 安全特性

- 启用了 `pyautogui.FAILSAFE`，将鼠标移到屏幕左上角可紧急中断
- 每个操作之间有延迟，方便观察
- 支持 Ctrl+C 中断

### 4. 技术要点总结

#### pyautogui 使用经验

1. **拖拽 vs 点击**
   - 在画图软件中，使用 `pyautogui.drag()` 而不是 `mouseDown() + moveTo() + mouseUp()`
   - `drag()` 会在移动过程中保持鼠标按下状态，适合绘制连续线条

2. **相对移动 vs 绝对移动**
   - `moveTo(x, y)` - 移动到绝对坐标
   - `drag(dx, dy)` - 相对当前位置移动
   - 绘制复杂图形时，相对移动更方便

3. **延迟设置**
   - `pyautogui.PAUSE` - 设置所有操作之间的默认暂停时间
   - `time.sleep()` - 在关键步骤之间添加额外延迟
   - `duration` 参数 - 控制移动/拖拽的持续时间

4. **安全机制**
   - `pyautogui.FAILSAFE = True` - 启用紧急停止功能（鼠标移到左上角）

## 待完成的工作

### 1. 游戏坐标测量

需要在实际的植物大战僵尸游戏中测量以下坐标：

- [ ] 植物卡槽的位置和间距
- [ ] 游戏网格的起始位置和单元格尺寸
- [ ] 铲子的位置
- [ ] 阳光的可能出现区域

**测量方法：**
1. 启动游戏并进入关卡
2. 运行 `python control/show_mouse_position.py`
3. 将鼠标移动到各个关键位置并记录坐标
4. 更新 `executor.py` 中的坐标常量

### 2. 植物映射配置

需要在游戏开始时确定：

- [ ] 当前关卡选择了哪些植物
- [ ] 每个植物在卡槽中的位置（索引）
- [ ] 创建植物名称到卡槽索引的映射字典

**示例：**
```python
plant_mapping = {
    "peashooter": 0,    # 豌豆射手在第1个卡槽
    "sunflower": 1,     # 向日葵在第2个卡槽
    "wallnut": 2,       # 坚果墙在第3个卡槽
    "cherrybomb": 3,    # 樱桃炸弹在第4个卡槽
    "repeater": 4       # 双发射手在第5个卡槽
}
```

### 3. 游戏状态识别

未来可能需要实现：

- [ ] 识别当前阳光数量
- [ ] 识别植物冷却状态
- [ ] 识别僵尸位置
- [ ] 识别已种植的植物位置

这些功能可能需要使用图像识别技术（如 OpenCV）。

### 4. LLM 集成

需要实现：

- [ ] 与 LLM 的通信接口
- [ ] 游戏状态的文本描述生成
- [ ] LLM 输出的解析和验证
- [ ] 错误处理和重试机制

### 5. 完整的游戏循环

需要实现：

- [ ] 游戏启动和初始化
- [ ] 主循环：观察 → LLM 决策 → 执行动作
- [ ] 关卡完成检测
- [ ] 游戏失败处理

## 技术难点和注意事项

### 1. 坐标精度

- 游戏窗口的位置可能会变化
- 需要考虑不同分辨率和窗口模式
- 可能需要实现窗口位置自动检测

### 2. 时序控制

- 植物种植有冷却时间
- 阳光收集需要及时
- 需要合理安排操作顺序和延迟

### 3. 错误处理

- 阳光不足时无法种植
- 格子已有植物时无法种植
- 需要验证操作是否成功

### 4. 性能优化

- 减少不必要的鼠标移动
- 批量操作的优化
- 避免过度频繁的操作

## 依赖安装

```bash
pip install pyautogui
```

pyautogui 会自动安装以下依赖：
- pymsgbox
- pytweening
- pyscreeze
- pygetwindow
- mouseinfo
- pyrect
- pyperclip

## 测试记录

### 2026-05-27 测试结果

**测试环境：**
- 操作系统：Windows 11 Home China 10.0.26200
- 屏幕分辨率：2560 x 1600
- Python 版本：3.x
- pyautogui 版本：0.9.54

**测试程序：** `test_mouse.py`

**测试结果：** ✅ 成功

- 画图软件成功打开
- 画笔工具成功选择（快捷键 'p'）
- 所有图形成功绘制在画布正确区域内
- 点击模式测试正常
- 坐标计算准确

**关键发现：**
1. 使用 `pyautogui.drag()` 可以正确绘制连续线条
2. 画布坐标需要精确测量，不能假设为全窗口
3. 选择工具（如画笔）可以使用快捷键，比点击更可靠

## 下一步计划

1. **启动植物大战僵尸游戏**
   - 测量游戏界面的实际坐标
   - 更新 `executor.py` 中的坐标常量

2. **验证游戏操作**
   - 在实际游戏中测试种植、铲除等操作
   - 调整延迟时间以适应游戏响应速度

3. **实现游戏状态读取**
   - 研究如何获取游戏状态（阳光、僵尸位置等）
   - 可能需要使用 OCR 或图像识别

4. **集成 LLM**
   - 设计游戏状态的文本描述格式
   - 实现与 LLM 的通信接口
   - 测试完整的决策-执行循环

## 参考资料

- [pyautogui 官方文档](https://pyautogui.readthedocs.io/)
- [植物大战僵尸游戏机制](https://plantsvszombies.fandom.com/)

## 联系信息

项目开发者：[待填写]
项目仓库：[待填写]

---

**最后更新：** 2026年5月27日
**文档版本：** 1.0
