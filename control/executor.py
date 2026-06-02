import pyautogui
import time


class GameExecutor:
    """
    游戏执行器，负责将高层次的游戏指令转换为鼠标点击操作
    """

    # 可配置的坐标常量
    # 卡槽起始位置和间距
    SLOT_START_X = 100  # 第一个卡槽的X坐标
    SLOT_START_Y = 50   # 卡槽的Y坐标
    SLOT_SPACING = 60   # 卡槽之间的间距

    # 游戏网格起始位置和间距
    GRID_START_X = 250  # 第一列的X坐标
    GRID_START_Y = 150  # 第一行的Y坐标
    CELL_WIDTH = 80     # 每格的宽度
    CELL_HEIGHT = 100   # 每格的高度

    # 铲子位置
    SHOVEL_X = 600
    SHOVEL_Y = 50

    # 点击延迟（秒）
    CLICK_DELAY = 0.1

    def __init__(self):
        """
        初始化执行器
        植物名称到卡槽索引的映射需要在游戏开始时手动设置
        """
        self.plant_to_slot = {}
        pyautogui.PAUSE = 0.05  # 设置pyautogui操作之间的默认暂停时间

    def set_plant_mapping(self, plant_mapping):
        """
        设置植物名称到卡槽索引的映射

        Args:
            plant_mapping: dict, 例如 {"peashooter": 0, "sunflower": 1, "wallnut": 2}
        """
        self.plant_to_slot = plant_mapping

    def click_slot(self, slot):
        """
        点击指定的卡槽

        Args:
            slot: int, 卡槽索引（从0开始）
        """
        x = self.SLOT_START_X + slot * self.SLOT_SPACING
        y = self.SLOT_START_Y
        pyautogui.click(x, y)
        time.sleep(self.CLICK_DELAY)

    def click_cell(self, row, col):
        """
        点击指定的网格单元

        Args:
            row: int, 行号（从0开始）
            col: int, 列号（从0开始）
        """
        x = self.GRID_START_X + col * self.CELL_WIDTH
        y = self.GRID_START_Y + row * self.CELL_HEIGHT
        pyautogui.click(x, y)
        time.sleep(self.CLICK_DELAY)

    def click_shovel(self):
        """
        点击铲子
        """
        pyautogui.click(self.SHOVEL_X, self.SHOVEL_Y)
        time.sleep(self.CLICK_DELAY)

    def collect_sun(self, x, y):
        """
        收集阳光

        Args:
            x: int, 阳光的X坐标
            y: int, 阳光的Y坐标
        """
        pyautogui.click(x, y)
        time.sleep(self.CLICK_DELAY)

    def plant(self, plant, row, col):
        """
        种植植物

        Args:
            plant: str, 植物名称
            row: int, 行号
            col: int, 列号
        """
        if plant not in self.plant_to_slot:
            raise ValueError(f"未知的植物类型: {plant}")

        slot = self.plant_to_slot[plant]
        self.click_slot(slot)
        self.click_cell(row, col)

    def remove_plant(self, row, col):
        """
        移除植物

        Args:
            row: int, 行号
            col: int, 列号
        """
        self.click_shovel()
        self.click_cell(row, col)

    def execute(self, actions):
        """
        执行一系列动作

        Args:
            actions: list, 动作列表，每个动作是一个字典
                例如: [
                    {"action": "plant", "plant": "peashooter", "row": 2, "col": 5},
                    {"action": "remove", "row": 1, "col": 3},
                    {"action": "collect_sun", "x": 300, "y": 400}
                ]
        """
        for action in actions:
            action_type = action.get("action")

            if action_type == "plant":
                plant = action.get("plant")
                row = action.get("row")
                col = action.get("col")
                self.plant(plant, row, col)

            elif action_type == "remove":
                row = action.get("row")
                col = action.get("col")
                self.remove_plant(row, col)

            elif action_type == "collect_sun":
                x = action.get("x")
                y = action.get("y")
                self.collect_sun(x, y)

            else:
                print(f"警告: 未知的动作类型 '{action_type}'")