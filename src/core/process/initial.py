
from core.common.log import get_logger
from core.yolo.detect import detect_objects
from core.common.tools import distance

import core.gui.custom_gui as gui

logger = get_logger()

def t():
    logger.info("this is a info message from initial")

def initial():
    logger.info("开始游戏参数初始化")
    gui.back_to_game()
    edge_init()

def edge_init():
    cache = []
    gui.move_to_direction(gui.Direction.LEFT_DOWN, duration=0.8)
    points = detect_objects()
    for p in points:
        point = p["center"]
        dis = distance(point, gui.Corner.LEFT_DOWN.value)
        logger.info(f"检测到点: {point}, 距离左下角: {dis}")
    
