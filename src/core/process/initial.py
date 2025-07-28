
from core.common.log import get_logger

import core.gui.custom_gui as gui

logger = get_logger()

def t():
    logger.info("this is a info message from initial")

def initial():
    logger.info("开始游戏参数初始化")
    gui.back_to_game()
    gui.move_to_direction(gui.Direction.LEFT_DOWN, duration=0.8)

