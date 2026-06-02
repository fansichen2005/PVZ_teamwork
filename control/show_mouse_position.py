import pyautogui
import time


def show_mouse_position():
    """
    实时显示鼠标坐标
    按 Ctrl+C 退出
    """
    print("=" * 50)
    print("实时鼠标坐标显示")
    print("=" * 50)
    print("将鼠标移动到画布的关键位置并记录坐标：")
    print("  1. 画布左上角")
    print("  2. 画布右下角")
    print("\n按 Ctrl+C 退出\n")

    try:
        while True:
            x, y = pyautogui.position()
            position_str = f"X: {x:4d}  Y: {y:4d}"
            print(position_str, end='')
            print('\r', end='')  # 回到行首
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n程序已退出")


if __name__ == "__main__":
    show_mouse_position()
