import pyautogui as pa
import random
import time
import logging
import asyncio
import concurrent.futures
from functools import partial
import random

from .geometry import fluctuate_number, distance, generate_bezier_curve
from .image_utils import ImageLocator
from yolo.detect import ObjectDetector

class MouseUtils:
    screen_width, screen_height = pa.size()
    image_locator = ImageLocator()  # 创建 ImageLocator 实例

    @staticmethod
    def click_image(*image_names, color_sensitive=False):
        """
        尝试点击一系列图像中的一个
        
        参数:
            image_names: 图像名称列表
            color_sensitive: 是否启用颜色敏感模式
            
        返回:
            如果找到并点击了图像返回 True，否则返回 False
        """
        max_names = 5
        names_display = image_names[:max_names]
        names_str = ', '.join(names_display)
        if len(image_names) > max_names:
            names_str += ', ...'
            
        logging.info(f"Attempting to click on images: [{names_str}]")
        location = MouseUtils.image_locator.locate_images(
            *image_names, 
            color_sensitive=color_sensitive
        )
        
        if location:
            center = pa.center(location)
            MouseUtils.move(center)
            pa.click()
            return center
        else:
            # logging.warning(f"Failed to find images: [{names_str}]")
            return None

    @staticmethod
    def radio_to_actual(radio_x, radio_y):
        return int(radio_x * MouseUtils.screen_width), int(radio_y * MouseUtils.screen_height)

    @staticmethod
    def move_to_left_up():
        MouseUtils.move_from_to((1/4, 1/4), (3/4, 3/4))

    @staticmethod
    def move_to_left_down():
        MouseUtils.move_from_to((1/4, 3/4), (3/4, 1/4))

    @staticmethod
    def move_to_right_up():
        MouseUtils.move_from_to((3/4, 1/4), (1/4, 3/4))

    @staticmethod
    def move_to_right_down():
        MouseUtils.move_from_to((3/4, 3/4), (1/4, 1/4))

    @staticmethod
    def move_from_to(start_point, end_point, duration=0.8, holding=0.01):
        d = fluctuate_number(duration)
        if start_point[0] < 1:
            start_x, start_y = MouseUtils.radio_to_actual(*start_point)
        else:
            start_x, start_y = start_point[0], start_point[1]
        if end_point[0] < 1:
            end_x, end_y = MouseUtils.radio_to_actual(*end_point)
        else:
            end_x, end_y = end_point[0], end_point[1]
        
        MouseUtils.move((start_x, start_y))
        pa.mouseDown()
        time.sleep(holding)
        
        MouseUtils.move((end_x, end_y))
        pa.mouseUp()
        time.sleep(0.1)

    @staticmethod
    def move(end_pos, duration=0.6):
        position = pa.position()
        if distance(position, end_pos) < 100:
            return
        
        duration = fluctuate_number(duration)
        start_pos = pa.position()
        if start_pos == end_pos:
            return
            
        pos_offset = fluctuate_number(30)
        end_pos = (end_pos[0] + pos_offset, end_pos[1] + pos_offset)
        dist = distance(start_pos, end_pos)

        if dist < 400:
            pa.moveTo(end_pos, duration=duration, _pause=False)
            return

        mid_x = (start_pos[0] + end_pos[0]) / 2
        mid_y = (start_pos[1] + end_pos[1]) / 2
        offset = random.randrange(80, 120)
        side = random.choice([-1, 1])
        control_point = (
            mid_x + side * offset * random.uniform(0.8, 1.2),
            mid_y + side * offset * random.uniform(0.8, 1.2)
        )

        curve_points = generate_bezier_curve(start_pos, end_pos, [control_point])
        duration_per_point = duration / len(curve_points)

        for point in curve_points:
            pa.moveTo(point[0], point[1], duration=duration_per_point, _pause=False)
            time.sleep(duration_per_point)

    @staticmethod
    async def detect_best_direction():
        directions_config = [
            ("left_up", MouseUtils.move_to_left_up, (0.355078125, 0.31805555555555554), -0.75),
            ("left_down", MouseUtils.move_to_left_down, (0.345703125, 0.5472222222222223), 0.74),
            ("right_up", MouseUtils.move_to_right_up, (0.669921875, 0.3638888888888889), 0.74),
            ("right_down", MouseUtils.move_to_right_down, (0.701171875, 0.49444444444444446), -0.75)
        ]
        random.shuffle(directions_config)
        
        
        MAX_DISTANCE = MouseUtils.screen_height * 0.265
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            loop = asyncio.get_running_loop()
            tasks = []
            
            for name, move_func, coords, slope in directions_config:
                move_func()
                screenshot = pa.screenshot()
                x, y = MouseUtils.radio_to_actual(*coords)
                
                task = loop.run_in_executor(
                    executor, 
                    partial(ObjectDetector.calculate_avg_distance_to_line, slope, x, y, screenshot)
                )
                tasks.append((name, move_func, task))
            
            for name, move_func, task in tasks:
                distance_val, projected_points = await task
                logging.info(f"{name.title().replace('_', ' ')}: {distance_val}")
                results[name] = (distance_val, projected_points, move_func)
        
        if not results:
            logging.info("No valid results found")
            return None, []
        
        best_direction_name, (min_distance, min_projected_points, best_move_func) = min(
            results.items(), 
            key=lambda item: item[1][0]
        )
        
        if min_distance < MAX_DISTANCE:
            logging.info(f"Best direction: {best_direction_name} with distance {min_distance}")
            return best_move_func, min_projected_points
        else:
            logging.info(f"No valid direction (min distance {min_distance} >= {MAX_DISTANCE})")
            return None, []