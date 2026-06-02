import ctypes
import os

ctypes.windll.user32.SetProcessDPIAware()

import cv2
import numpy as np
from PIL import ImageGrab
from ultralytics import YOLO
import time
import json
import torch
import torch.nn as nn
import torchvision.transforms as transforms

# =========================================================
# 当前脚本所在文件夹
# =========================================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================================================
# 加载YOLO模型（同文件夹）
# =========================================================
yolo_model_path = os.path.join(CURRENT_DIR, "best.pt")
if not os.path.exists(yolo_model_path):
    raise FileNotFoundError(f"找不到YOLO模型：{yolo_model_path}\n请把模型放在脚本同一文件夹")
model = YOLO(yolo_model_path)

# =========================================================
# 类别名称
# =========================================================
CLASS_NAMES = [
    "sunflower",
    "repeater",
    "sun",
    "zombie",
    "potato_mine",
    "snowpea",
    "peashooter",
    "earthed_potato_mine",
    "nut",
    "cherry_bomb",
    "flag_zombie",
    "conehead_zombie",
    "pole_vaulting_zombie",
    "buckethead_zombie",
    "newspaper_zombie"
]

# =========================================================
# CNN数字识别网络
# =========================================================
class DigitCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.fc = nn.Sequential(
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# =========================================================
# 加载CNN模型
# =========================================================
device = torch.device("cpu")
digit_model = DigitCNN()
cnn_model_path = os.path.join(CURRENT_DIR, "pvz_digit_cnn.pth")
if not os.path.exists(cnn_model_path):
    raise FileNotFoundError(f"找不到CNN模型：{cnn_model_path}\n请把模型放在脚本同一文件夹")
digit_model.load_state_dict(torch.load(cnn_model_path, map_location=device))
digit_model.eval()

# =========================================================
# 图像预处理
# =========================================================
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((28,28)),
    transforms.ToTensor()
])

# =========================================================
# 鼠标变量
# =========================================================
drawing = False
ix, iy = -1, -1
fx, fy = -1, -1

# =========================================================
# 鼠标回调
# =========================================================
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, fx, fy, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        fx, fy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            fx, fy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        fx, fy = x, y

# =========================================================
# 框选区域
# =========================================================
def select_region(window_name):
    global ix, iy, fx, fy
    ix, iy, fx, fy = -1, -1, -1, -1
    screen = ImageGrab.grab()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    clone = screen.copy()
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, draw_rectangle)
    print(f"\n请框选 {window_name}")
    print("ENTER确认")

    while True:
        temp = clone.copy()
        if ix != -1:
            cv2.rectangle(temp, (ix, iy), (fx, fy), (0,255,0), 2)
        cv2.imshow(window_name, temp)
        key = cv2.waitKey(1)
        if key == 13:
            break

    cv2.destroyWindow(window_name)
    x1 = min(ix, fx)
    y1 = min(iy, fy)
    x2 = max(ix, fx)
    y2 = max(iy, fy)
    return (x1, y1, x2, y2)

# =========================================================
# 动态网格映射
# =========================================================
def pixel_to_grid(x, y, lawn_bbox):
    lawn_x1, lawn_y1, lawn_x2, lawn_y2 = lawn_bbox
    width = lawn_x2 - lawn_x1
    height = lawn_y2 - lawn_y1
    cell_width = width / 9
    cell_height = height / 5
    col = int((x - lawn_x1) / cell_width)
    row = int((y - lawn_y1) / cell_height)
    col = max(0, min(8, col))
    row = max(0, min(4, row))
    return row, col

# =========================================================
# CNN识别阳光数字
# =========================================================
def recognize_sunlight_cnn(ocr_bbox):
    x1, y1, x2, y2 = ocr_bbox
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    frame = np.array(img)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((2,2), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    vertical_sum = np.sum(thresh, axis=0)

    digit_regions = []
    in_digit = False
    start = 0
    for i in range(len(vertical_sum)):
        if vertical_sum[i] > 0 and not in_digit:
            in_digit = True
            start = i
        elif vertical_sum[i] == 0 and in_digit:
            in_digit = False
            end = i
            if end - start > 3:
                digit_regions.append((start, end))
    if in_digit:
        digit_regions.append((start, len(vertical_sum)-1))

    result = ""
    for start, end in digit_regions:
        digit = thresh[:, start:end]
        ys, xs = np.where(digit > 0)
        if len(ys) == 0:
            continue
        y_min = np.min(ys)
        y_max = np.max(ys)
        digit = digit[y_min:y_max+1, :]

        h, w = digit.shape
        size = max(h, w) + 10
        canvas = np.zeros((size, size), dtype=np.uint8)
        x_offset = (size - w) // 2
        y_offset = (size - h) // 2
        canvas[y_offset:y_offset+h, x_offset:x_offset+w] = digit

        canvas = cv2.resize(canvas, (28,28))
        tensor = transform(canvas).unsqueeze(0)

        with torch.no_grad():
            output = digit_model(tensor)
            pred = output.argmax(1).item()  # 这里是你原本正确的代码
        result += str(pred)

    if result == "":
        result = "0"
    return result

# =========================================================
# 自适应显示
# =========================================================
def resize_display(img):
    h, w = img.shape[:2]
    max_w = 1400
    max_h = 900
    scale = min(max_w / w, max_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = cv2.resize(img, (new_w, new_h))
    return resized

# =========================================================
# 主程序
# =========================================================
print("\n========== PVZ AI 输入层 ==========")

game_bbox = select_region("Game Region")
lawn_bbox = select_region("Lawn Region")
ocr_bbox = select_region("Sunlight Region")

print("\n开始实时识别...")
print("ESC退出\n")

cv2.namedWindow("PVZ Detection", cv2.WINDOW_NORMAL)

# =========================================================
# 输出文件：JSON 和 TXT 都保存在当前文件夹
# =========================================================
JSON_OUTPUT_PATH = os.path.join(CURRENT_DIR, "pvz_data.json")
TXT_OUTPUT_PATH = os.path.join(CURRENT_DIR, "pvz_data.txt")

# =========================================================
# 主循环
# =========================================================
while True:
    loop_start = time.time()

    game_x1, game_y1, game_x2, game_y2 = game_bbox
    img = ImageGrab.grab(bbox=(game_x1, game_y1, game_x2, game_y2))
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    results = model.predict(frame, conf=0.5, verbose=False)
    data = {
        "sunlight": 0,
        "plants": [],
        "zombie": [],
        "falling_sun": []
    }
    boxes = results[0].boxes

    for box in boxes:
        cls_id = int(box.cls[0])
        name = CLASS_NAMES[cls_id]
        x_min, y_min, x_max, y_max = map(int, box.xyxy[0])

        if name in [
            "sunflower", "repeater", "potato_mine", "snowpea",
            "peashooter", "earthed_potato_mine", "nut", "cherry_bomb"
        ]:
            cx = int((x_min + x_max) / 2)
            cy = int((y_min + y_max) / 2)
            abs_x = cx + game_x1
            abs_y = cy + game_y1
            row, col = pixel_to_grid(abs_x, abs_y, lawn_bbox)
            data["plants"].append({
                "type": name,
                "row": row,
                "col": col
            })

        elif "zombie" in name:
            cx = int((x_min + x_max) / 2)
            cy = int(y_min + (y_max - y_min) * 2 / 3)
            abs_x = cx + game_x1
            abs_y = cy + game_y1
            row, col = pixel_to_grid(abs_x, abs_y, lawn_bbox)
            data["zombie"].append({
                "type": name,
                "row": row,
                "col": col
            })

        elif name == "sun":
            cx = int((x_min + x_max) / 2)
            cy = int((y_min + y_max) / 2)
            abs_x = cx + game_x1
            abs_y = cy + game_y1
            data["falling_sun"].append({"x": abs_x, "y": abs_y})

        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0,255,0), 2)
        cv2.putText(frame, name, (x_min, y_min - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    sunlight = recognize_sunlight_cnn(ocr_bbox)
    data["sunlight"] = sunlight
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    print(json_str)

    # 写入文件
    with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    with open(TXT_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(json_str)

    display = resize_display(frame)
    cv2.imshow("PVZ Detection", display)

    key = cv2.waitKey(1)
    if key == 27:
        break

    elapsed = time.time() - loop_start
    remain = 0.3 - elapsed
    if remain > 0:
        time.sleep(remain)

cv2.destroyAllWindows()