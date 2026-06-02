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