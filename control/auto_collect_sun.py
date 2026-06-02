# -*- coding: utf-8 -*-
"""
阳光自动收集器
实时读取视觉识别模块输出的 pvz_data.json，自动点击所有掉落的阳光
"""

import sys
import os
import json
import time
import pyautogui
from pathlib import Path

# 修复 Windows 终端编码问题
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class SunCollector:
    """阳光自动收集器"""

    def __init__(self, json_path="../pvz_data.json"):
        """
        初始化收集器

        Args:
            json_path: pvz_data.json 文件路径（相对于 control/ 目录）
        """
        self.json_path = Path(__file__).parent / json_path
        self.click_delay = 0.05  # 点击间隔（秒）
        self.check_interval = 0.1  # 检查 JSON 文件的间隔（秒）
        self.collected_count = 0  # 已收集阳光数量统计

        pyautogui.FAILSAFE = True  # 鼠标移到屏幕左上角可紧急中断
        pyautogui.PAUSE = 0.02

        print("=" * 60)
        print("  阳光自动收集器")
        print("  提示：将鼠标移至屏幕左上角可紧急中断")
        print("  按 Ctrl+C 退出程序")
        print("=" * 60)

    def read_game_data(self):
        """
        读取 pvz_data.json 文件

        Returns:
            dict: 游戏数据，读取失败返回 None
        """
        try:
            if not self.json_path.exists():
                return None

            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data

        except json.JSONDecodeError:
            # JSON 文件可能正在被写入，跳过本次读取
            return None
        except Exception as e:
            print(f"读取文件失败: {e}")
            return None

    def collect_sun(self, x, y):
        """
        点击指定坐标收集阳光

        Args:
            x: int, 阳光的 X 坐标
            y: int, 阳光的 Y 坐标
        """
        try:
            pyautogui.click(x, y)
            self.collected_count += 1
            time.sleep(self.click_delay)
        except Exception as e:
            print(f"点击失败 ({x}, {y}): {e}")

    def process_falling_sun(self, falling_sun_list):
        """
        处理掉落阳光列表，逐个点击收集

        Args:
            falling_sun_list: list, 阳光坐标列表
                例如: [{"x": 619, "y": 142}, {"x": 197, "y": 417}]
        """
        if not falling_sun_list:
            return

        count = len(falling_sun_list)
        print(f"\r[收集] 发现 {count} 个阳光", end="", flush=True)

        for sun in falling_sun_list:
            x = sun.get("x")
            y = sun.get("y")

            if x is not None and y is not None:
                self.collect_sun(x, y)

        if count > 0:
            print(f" → 已收集 (总计: {self.collected_count})")

    def run(self):
        """
        主循环：持续监控 JSON 文件并自动收集阳光
        """
        print(f"\n正在监控文件: {self.json_path.absolute()}")
        print("等待视觉识别数据...\n")

        last_mtime = 0  # 文件上次修改时间

        try:
            while True:
                # 检查文件是否存在且已更新
                if self.json_path.exists():
                    current_mtime = self.json_path.stat().st_mtime

                    # 只有文件更新时才读取（避免重复处理相同数据）
                    if current_mtime > last_mtime:
                        last_mtime = current_mtime

                        data = self.read_game_data()
                        if data:
                            falling_sun = data.get("falling_sun", [])
                            self.process_falling_sun(falling_sun)

                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print("\n\n程序已停止")
            print(f"本次运行共收集 {self.collected_count} 个阳光")
            print("=" * 60)


def main():
    """
    主函数

    使用方法：
        python control/auto_collect_sun.py

    前提条件：
        1. 视觉识别程序 (visual_program.py) 已运行
        2. pvz_data.json 文件正在被实时更新
    """
    collector = SunCollector()
    collector.run()


if __name__ == "__main__":
    main()
