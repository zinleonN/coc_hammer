import pyautogui as pa
import logging

from src.common.mouse_utils import MouseUtils
from src.common.image_utils import ImageLocator

class DonationManager:
    def __init__(self):
        self.army_names = [
            "donate_army_giant", "donate_army_miner", "donate_army_archer", 
            "donate_army_barbarian", "donate_army_goblin", "donate_army_wall_breaker",
            "donate_army_balloon", "donate_army_wizard", "donate_army_healer",
            "donate_army_dragon", "donate_army_pekka", "donate_army_baby_dragon",
            "donate_army_miner", "donate_army_electro_dragon", "donate_army_yeti",
            "donate_army_dragon_rider", "donate_army_electro_titan", "donate_army_root_rider",
            "donate_army_thrower", "donate_army_minion", "donate_army_hog_rider",
            "donate_army_valkyrie", "donate_army_golem", "donate_army_electro_wizard",
            "donate_lighting", "donate_poison"
        ]

    def random_donate(self):
        left_loc = ImageLocator().locate_images("donate_army_hog_rider")
        right_loc = ImageLocator().locate_images("donate_army_giant")
        
        if not left_loc or not right_loc:
            return False
            
        MouseUtils.move(pa.center(left_loc))
        pa.mouseDown()
        MouseUtils.move(pa.center(right_loc))
        pa.mouseUp()
        
        while MouseUtils.click_image(*self.army_names, color_sensitive=True):
            pass
            
        return True

    def process_donation(self):
        logging.info("Starting donation sequence...")
        need_resource = False
        
        if not MouseUtils.click_image("donate_start"):
            return False
            
        while True:
            if MouseUtils.click_image("donate_1"):
                self.random_donate()
                need_resource = True
            elif MouseUtils.click_image("donate_locate"):
                continue
            else:
                MouseUtils.click_image("donate_back")
                return need_resource