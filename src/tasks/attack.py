import asyncio
import pyautogui as pa
import logging
import random

from src.common.mouse_utils import MouseUtils
from src.common.image_utils import ImageLocator

class AttackManager:
    def __init__(self):
        self.attack_army_names = [
            "attack_army_special_goblin", "attack_army_goblin", 
            "attack_army_dragon", "attack_army_super_goblin"
        ]
        self.attack_hero_names = [
            "attack_hero_archer_queen", "attack_hero_minion_prince",
            "attack_hero_grand_warden"
        ]

    async def choose_suitable_attack_target(self):
        logging.info("attack: waitting the cloud...")
        while True:
            if not ImageLocator().locate_images("attack_next_target"):
                logging.debug("Waiting for next target button...")
                pa.sleep(1)
                continue
                
            for _ in range(10):
                pa.scroll(-500)
                
            move_func, projected_points = await MouseUtils.detect_best_direction()
            if move_func:
                logging.info(f"Best move function: {move_func.__name__}")
                return move_func, projected_points
                
            logging.info("attack: No suitable attack target found. Trying next...")
            MouseUtils.click_image("attack_next_target")

    def place_armies(self, move_func, projected_points):
        move_func()
        
        for name in self.attack_army_names:
            location = ImageLocator().locate_images(name, color_sensitive=True)
            if not location:
                continue
                
            pa.click(pa.center(location), duration=0.2)
            
            while ImageLocator().locate_images(name, color_sensitive=True):
                target_point = random.choice(projected_points)
                pa.click(*target_point, duration=0.2)
                pa.sleep(0.1)
                pa.click()
                pa.sleep(0.1)
                pa.click()

    def place_heroes(self, projected_points):
        target_point = random.choice(projected_points)

        for hero_name in self.attack_hero_names:
            if MouseUtils.click_image(hero_name):
                pa.click(*target_point, duration=0.3)

    def execute_attack(self):
        logging.info("attack: Starting sequence")
        
        if not MouseUtils.click_image("attack_1", "attack_2"):
            return False
        if not MouseUtils.click_image("search_1"):
            return False
        move_func, projected_points = asyncio.run(self.choose_suitable_attack_target())
        
        self.place_armies(move_func, projected_points)
        self.place_heroes(projected_points)
    
        logging.info("attack: Waiting for attack to complete...")
        while True:
            pa.sleep(6)
            if ImageLocator().locate_images("attack_back"):
                pa.sleep(3)
                MouseUtils.click_image("attack_back")
                pa.sleep(8)
                
                if ImageLocator().locate_images("attack_confirm_resource"):
                    pa.click(pa.center(ImageLocator().locate_images("attack_confirm_resource")))
                return True