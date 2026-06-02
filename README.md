# PVZ AI 视觉识别程序
基于 **YOLO 目标检测 + CNN 数字识别** 的植物大战僵尸实时视觉分析程序，自动识别游戏内植物、僵尸、阳光数量，并输出结构化数据。

---

## 一、程序功能
1. **实时目标检测**
   - 识别植物：向日葵、双重射手、豌豆射手、坚果、樱桃炸弹等
   - 识别僵尸：普通僵尸、旗帜僵尸、路障僵尸、铁桶僵尸等
   - 识别掉落阳光，实时定位坐标

2. **阳光数值识别**
   - 使用 CNN 模型精准识别游戏内阳光数字
   - 输出稳定、可读的阳光数值

3. **网格坐标映射**
   - 自动将游戏画面映射为 5×9 草坪网格
   - 输出植物/僵尸所在行列坐标

4. **数据自动输出**
   - 实时输出 `pvz_data.json` 结构化数据
   - 同步输出 `pvz_data.txt` 日志文件
   - 所有文件自动保存在程序同文件夹

5. **可视化界面**
   - 实时显示检测框与类别名称
   - 支持框选游戏区域、草坪区域、阳光区域

---

## 二、运行环境与依赖安装
### 1. 环境要求
- Python 3.8 ~ 3.11
- Windows 系统（推荐）

### 2. 一键安装依赖
在**程序文件夹内**打开终端，运行：
```bash
pip install -r requirements.txt
```

### 3. 手动安装（无 requirements.txt）
```bash
pip install opencv-python
pip install numpy
pip install pillow
pip install torch torchvision
pip install ultralytics
```

---

## 三、文件结构说明
**必须将所有文件放在同一个文件夹内**
```
PVZ_visual_part/
├─ visual_program.py    # 主程序
├─ best.pt              # YOLO 模型权重
├─ pvz_digit_cnn.pth    # CNN 阳光识别模型
├─ pvz_data.json        # 自动输出（运行后生成）
└─ pvz_data.txt         # 自动输出（运行后生成）
```

---

## 四、使用方法
1. 打开植物大战僵尸游戏
2. 运行 `visual_program.py`
3. 按提示依次框选三个区域：
   - Game Region：游戏窗口整体区域
   - Lawn Region：草坪种植区域
   - Sunlight Region：阳光数字显示区域
4. 按 `ENTER` 确认，程序开始实时识别
5. 按 `ESC` 退出程序

---

## 五、输出数据格式（JSON）
```json
{
    "sunlight": "150",
    "plants": [
        {"type": "sunflower", "row": 1, "col": 2}
    ],
    "zombie": [
        {"type": "zombie", "row": 2, "col": 8}
    ],
    "falling_sun": [
        {"x": 520, "y": 310}
    ]
}
```

---

## 六、注意事项
1. 游戏窗口**不要最小化**，保持可见
2. 框选区域尽量精准，否则识别会下降
3. 模型文件名称必须为：`best.pt`、`pvz_digit_cnn.pth`
4. 输出文件自动保存在程序所在文件夹，无需手动设置路径
5. 首次运行加载模型较慢，属于正常现象

---

## 七、支持识别列表
### 植物
sunflower、repeater、peashooter、snowpea、nut、cherry_bomb、potato_mine、earthed_potato_mine

### 僵尸
zombie、flag_zombie、conehead_zombie、buckethead_zombie、newspaper_zombie、pole_vaulting_zombie

### 其他
sun（阳光）

---

## 八、鼠标控制模块 (control/)

将 LLM 输出的高层次指令转换为精确的鼠标操作，实现种植、铲除、收集阳光等游戏操作。

### 核心组件

#### 1. GameExecutor (executor.py)
游戏执行器类，提供以下方法：
- `plant(plant, row, col)` - 种植植物
- `remove_plant(row, col)` - 铲除植物
- `collect_sun(x, y)` - 收集阳光
- `execute(actions)` - 批量执行指令列表

**LLM 指令格式：**
```python
actions = [
    {"action": "plant", "plant": "peashooter", "row": 2, "col": 5},
    {"action": "remove", "row": 1, "col": 3},
    {"action": "collect_sun", "x": 300, "y": 400}
]
```

#### 2. 阳光自动收集器 (auto_collect_sun.py)
独立运行的阳光收集程序，**无需 LLM 决策**：
- 实时监控 `pvz_data.json` 文件
- 自动读取 `falling_sun` 数组中的阳光坐标
- 逐个点击收集所有掉落的阳光
- 最高优先级，不影响 LLM 决策流程

**运行方式：**
```bash
# 先启动视觉识别程序
python visual_program.py

# 在另一个终端启动阳光收集器
python control/auto_collect_sun.py
```

**设计理念：** 收集阳光是零成本的高频操作，不需要 LLM 参与决策，直接响应视觉识别结果即可。

### 测试工具

#### LLM 指令模拟测试
```bash
python control/llm_simulation_test.py
```
自动打开画图软件，执行 10 条预设的 LLM 指令，演示完整的执行流程。

#### 阳光收集器测试
```bash
# 终端1：启动阳光收集器
python control/auto_collect_sun.py

# 终端2：运行测试数据生成器
python control/test_sun_collector.py
```
测试程序会每 2-4 秒生成随机阳光坐标，观察收集器是否自动点击。

#### 鼠标坐标显示工具
```bash
python control/show_mouse_position.py
```
实时显示鼠标坐标，用于测量游戏界面关键位置。

### 依赖安装
```bash
pip install pyautogui
```

---

## 九、完整工作流程

```
1. 视觉识别 (visual_program.py)
   ↓
   实时输出 pvz_data.json
   ↓
2. 阳光收集器 (auto_collect_sun.py) ← 自动收集阳光
   ↓
3. LLM 决策层（待实现）← 读取游戏状态，制定策略
   ↓
4. 游戏执行器 (executor.py) ← 执行种植、铲除等操作
```

---

## 十、项目进度

- [x] 视觉识别模块 (YOLO + CNN)
- [x] 鼠标控制基础框架
- [x] 阳光自动收集器
- [x] LLM 指令模拟测试
- [ ] 游戏坐标精确测量
- [ ] LLM 决策层实现
- [ ] 完整系统集成测试

详见 [PROJECT_LOG.md](PROJECT_LOG.md)