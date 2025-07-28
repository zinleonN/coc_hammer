import logging
import cv2
import time
import numpy as np
import pyautogui as pa
import random
from pathlib import Path
from enum import Enum as enum

from core.common.tools import fluctuate_number, distance
from core.common.file import image_path
from core.common.log import get_logger

logger = get_logger()

screen_width, screen_height = pa.size()

class Direction(enum):
    LEFT_UP = (screen_width / 6 * 2, screen_height / 6 * 2)
    LEFT_DOWN = (screen_width / 6 * 2, screen_height / 6 * 4)
    RIGHT_UP = (screen_width / 6 * 4, screen_height / 6 * 2)
    RIGHT_DOWN = (screen_width / 6 * 4, screen_height / 6 * 4)

def sleep(n):
    n = fluctuate_number(n)
    time.sleep(n)

def locate_images(*image_names, confidence=0.8, color_sensitive=False, min_saturation=40):
    sleep(0.2)
    
    for name in image_names:
        path = image_path(name)
        if not path: continue

        if not color_sensitive:
            try:
                location = pa.locateOnScreen(path, confidence=confidence)
                if location:
                    return location
            except:
                continue
        else:
            screen = pa.screenshot()
            screen = np.array(screen)
            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
            template = cv2.imread(path)

            screen_hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
            template_hsv = cv2.cvtColor(template, cv2.COLOR_BGR2HSV)
            res = cv2.matchTemplate(screen_hsv, template_hsv, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val >= confidence:
                h, w = template.shape[:2]
                left, top = max_loc
                matched = screen_hsv[top:top+h, left:left+w]
                if matched.shape[:2] == (h, w):
                    mean_s = matched[...,1].mean()
                    if mean_s >= min_saturation:
                        return (left, top, w, h)
        
        logging.debug(f"failed locate {name}")
        return None

def back_to_game():
    import pygetwindow as gw

    # 获取所有打开的窗口
    windows = gw.getWindowsWithTitle('部落冲突')

    if windows:
        window = windows[0]
        window.activate()  # 切换到该窗口
        sleep(1)
        pull_up_camera()
        logger.info("已切换到游戏窗口")
    else:
        print("窗口未找到")
        logger.error("窗口未找到，请确保游戏窗口已打开")
        raise RuntimeError("窗口未找到，请确保游戏窗口已打开")
        exit(-1)
    
def pull_up_camera():
    for _ in range(8):
        pa.scroll(-800)
        

def move(x, y, duration=0.4):
    def generate_bezier_curve(start, end, control_points, num_points=100):
        points = []
        for i in range(num_points + 1):
            t = i / num_points
            x = (1-t)**2 * start[0] + 2*(1-t)*t * control_points[0][0] + t**2 * end[0]
            y = (1-t)**2 * start[1] + 2*(1-t)*t * control_points[0][1] + t**2 * end[1]
            points.append((x, y))
        return points

    current_x, current_y = pa.position()
    if distance((current_x, current_y), (x, y)) < 100:
        return
    
    pos_offset = fluctuate_number(20)
    x, y = x + pos_offset, y + pos_offset

    if distance((current_x, current_y), (x, y)) < 400:
        pa.moveTo(x, y, duration=duration)
        return
    else:
        mid_x = (current_x + x) / 2
        mid_y = (current_y + y) / 2
        offset = random.randrange(80, 120)
        side = random.choice([-1, 1])
        control_point = (
            mid_x + side * offset * random.uniform(0.8, 1.2),
            mid_y + side * offset * random.uniform(0.8, 1.2)
        )

        curve_points = generate_bezier_curve((current_x, current_y), (x, y), [control_point])
        duration_per_point = duration / len(curve_points)

        for point in curve_points:
            pa.moveTo(point[0], point[1], duration=duration_per_point, _pause=False)
            time.sleep(duration_per_point)

def grag(start_pos, end_pos, duration=0.7):
    move(start_pos[0], start_pos[1])
    pa.mouseDown()
    sleep(0.02)
    move(end_pos[0], end_pos[1], duration)
    pa.mouseUp()
    sleep(0.02)

def move_to_direction(direction, duration=0.8):
    logger.debug(f"move to direction: {direction}")
    if direction == Direction.LEFT_UP:
        grag(Direction.LEFT_UP.value, Direction.RIGHT_DOWN.value,  duration)
    elif direction == Direction.LEFT_DOWN:
        grag(Direction.LEFT_DOWN.value, Direction.RIGHT_UP.value, duration)
    elif direction == Direction.RIGHT_UP:
        grag(Direction.RIGHT_UP.value, Direction.LEFT_DOWN.value, duration)
    elif direction == Direction.RIGHT_DOWN:
        grag(Direction.RIGHT_DOWN.value, Direction.LEFT_UP.value, duration)