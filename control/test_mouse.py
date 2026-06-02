import pyautogui
import time
import subprocess


def open_paint():
    """
    打开Windows画图软件
    """
    print("正在打开画图软件...")
    subprocess.Popen("mspaint.exe")
    time.sleep(2)  # 等待画图软件启动
    print("画图软件已打开")


def select_brush_tool():
    """
    选择画笔工具
    注意：这个坐标需要根据实际画图软件界面调整
    """
    # 画笔工具通常在工具栏的左侧
    # 这里使用一个通用的位置，可能需要调整
    print("选择画笔工具...")
    # 可以通过快捷键选择画笔
    pyautogui.press('p')  # 'p' 是画笔工具的快捷键
    time.sleep(0.3)


def draw_square(x, y, size):
    """
    绘制一个正方形

    Args:
        x: int, 起始X坐标
        y: int, 起始Y坐标
        size: int, 正方形边长
    """
    print(f"绘制正方形: 起点({x}, {y}), 边长{size}")
    pyautogui.moveTo(x, y)
    pyautogui.drag(size, 0, duration=0.5)  # 向右
    pyautogui.drag(0, size, duration=0.5)  # 向下
    pyautogui.drag(-size, 0, duration=0.5)  # 向左
    pyautogui.drag(0, -size, duration=0.5)  # 向上


def draw_circle(center_x, center_y, radius):
    """
    绘制一个圆形（近似）

    Args:
        center_x: int, 圆心X坐标
        center_y: int, 圆心Y坐标
        radius: int, 半径
    """
    print(f"绘制圆形: 圆心({center_x}, {center_y}), 半径{radius}")
    import math

    # 计算圆上的点
    points = []
    for angle in range(0, 360, 5):  # 更密集的点
        rad = math.radians(angle)
        x = center_x + radius * math.cos(rad)
        y = center_y + radius * math.sin(rad)
        points.append((x, y))

    # 移动到起点并开始绘制
    pyautogui.moveTo(points[0][0], points[0][1])

    # 使用拖拽绘制圆
    for i in range(1, len(points)):
        dx = points[i][0] - points[i-1][0]
        dy = points[i][1] - points[i-1][1]
        pyautogui.drag(dx, dy, duration=0.01)

    # 回到起点闭合圆
    dx = points[0][0] - points[-1][0]
    dy = points[0][1] - points[-1][1]
    pyautogui.drag(dx, dy, duration=0.01)


def draw_line(x1, y1, x2, y2):
    """
    绘制一条直线

    Args:
        x1, y1: int, 起点坐标
        x2, y2: int, 终点坐标
    """
    print(f"绘制直线: ({x1}, {y1}) -> ({x2}, {y2})")
    pyautogui.moveTo(x1, y1)
    pyautogui.drag(x2 - x1, y2 - y1, duration=0.5)


def draw_zigzag(start_x, start_y, width, height, segments):
    """
    绘制锯齿形

    Args:
        start_x, start_y: int, 起点坐标
        width: int, 总宽度
        height: int, 锯齿高度
        segments: int, 锯齿数量
    """
    print(f"绘制锯齿形: 起点({start_x}, {start_y}), {segments}个锯齿")
    segment_width = width / segments

    pyautogui.moveTo(start_x, start_y)

    for i in range(segments):
        x = start_x + (i + 0.5) * segment_width
        y = start_y - height if i % 2 == 0 else start_y
        pyautogui.drag(x - pyautogui.position()[0], y - pyautogui.position()[1], duration=0.2)

    # 最后回到终点
    final_x = start_x + width
    final_y = start_y
    pyautogui.drag(final_x - pyautogui.position()[0], final_y - pyautogui.position()[1], duration=0.2)


def draw_grid(start_x, start_y, rows, cols, cell_size):
    """
    绘制网格

    Args:
        start_x, start_y: int, 起点坐标
        rows: int, 行数
        cols: int, 列数
        cell_size: int, 单元格大小
    """
    print(f"绘制网格: {rows}行 x {cols}列, 单元格大小{cell_size}")

    # 绘制横线
    for i in range(rows + 1):
        y = start_y + i * cell_size
        draw_line(start_x, y, start_x + cols * cell_size, y)
        time.sleep(0.1)

    # 绘制竖线
    for i in range(cols + 1):
        x = start_x + i * cell_size
        draw_line(x, start_y, x, start_y + rows * cell_size)
        time.sleep(0.1)


def test_click_pattern():
    """
    测试点击模式 - 模拟游戏中的卡槽和网格点击
    """
    print("\n测试点击模式（模拟游戏操作）")

    # 模拟点击卡槽位置
    print("模拟点击卡槽...")
    slot_start_x = 100
    slot_y = 100
    slot_spacing = 60

    for i in range(5):
        x = slot_start_x + i * slot_spacing
        pyautogui.click(x, slot_y)
        print(f"  点击卡槽 {i}: ({x}, {slot_y})")
        time.sleep(0.3)

    time.sleep(1)

    # 模拟点击网格位置
    print("模拟点击网格...")
    grid_start_x = 300
    grid_start_y = 200
    cell_width = 80
    cell_height = 100

    for row in range(3):
        for col in range(5):
            x = grid_start_x + col * cell_width
            y = grid_start_y + row * cell_height
            pyautogui.click(x, y)
            print(f"  点击网格 ({row}, {col}): ({x}, {y})")
            time.sleep(0.2)


def main():
    """
    主测试函数
    """
    print("=" * 50)
    print("鼠标点击功能测试程序")
    print("=" * 50)

    # 安全提示
    print("\n注意: 程序将在3秒后开始执行")
    print("如需中断，请将鼠标移动到屏幕左上角")
    pyautogui.FAILSAFE = True

    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    # 打开画图软件
    open_paint()

    print("\n请手动最大化画图窗口，程序将在5秒后开始绘制")
    time.sleep(5)

    # 获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    print(f"屏幕尺寸: {screen_width} x {screen_height}")

    # 画布区域坐标（根据实际测量）
    canvas_left = 728
    canvas_top = 456
    canvas_right = 1499
    canvas_bottom = 1363
    canvas_width = canvas_right - canvas_left
    canvas_height = canvas_bottom - canvas_top

    print(f"画布区域: ({canvas_left}, {canvas_top}) 到 ({canvas_right}, {canvas_bottom})")
    print(f"画布尺寸: {canvas_width} x {canvas_height}")

    # 设置绘图起始位置（画布左上角 + 边距）
    canvas_x = canvas_left + 50
    canvas_y = canvas_top + 50

    print("\n开始绘制测试图形...")

    # 选择画笔工具
    select_brush_tool()

    # 测试1: 绘制正方形
    draw_square(canvas_x, canvas_y, 100)
    time.sleep(0.5)

    # 测试2: 绘制圆形
    draw_circle(canvas_x + 200, canvas_y + 50, 50)
    time.sleep(0.5)

    # 测试3: 绘制直线
    draw_line(canvas_x, canvas_y + 150, canvas_x + 300, canvas_y + 150)
    time.sleep(0.5)

    # 测试4: 绘制锯齿形
    draw_zigzag(canvas_x, canvas_y + 200, 200, 30, 5)
    time.sleep(0.5)

    # 测试5: 绘制网格（模拟游戏网格）
    draw_grid(canvas_x + 350, canvas_y, 5, 9, 40)
    time.sleep(0.5)

    # 测试6: 点击模式测试
    test_click_pattern()

    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        import traceback
        traceback.print_exc()
