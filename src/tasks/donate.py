import pyautogui as pa
import logging

from src.common.mouse_utils import MouseUtils
from src.common.image_utils import ImageLocator

class DonationManager:
    def __init__(self):
        self.army_names = [
            "donate_army_balloon", "donate_army_dragon", "donate_army_archer", 
            "donate_army_barbarian", "donate_army_goblin", "donate_army_wall_breaker",
            "donate_army_giant", "donate_army_wizard", "donate_army_healer",
            "donate_army_pekka", "donate_army_baby_dragon",

            "donate_army_minion", "donate_army_hog_rider", "donate_army_valkyrie",
            "donate_army_golem",


            "donate_lighting", "donate_poison",
        ]

    def random_donate(self):
        right_pos = (0,9999)
        left_pos = (9999,9999)

        for name in self.army_names:
            center = MouseUtils.image_locator.locate_images(name)
            if center == None: continue
            if center[0] > right_pos[0] and center[1] < right_pos[1]:
                right_pos = pa.center(center)
            if center[0] < left_pos[0] and center[1] < left_pos[1]:
                left_pos = pa.center(center)
        logging.info(f"right_pos: {right_pos}")
        logging.info(f"left_pos: {left_pos}")
        
        moved = False

        while True:
            center = MouseUtils.click_image(*self.army_names, color_sensitive=True)
            if center == None and moved == False :
                MouseUtils.move_from_to(right_pos, left_pos)
                moved = True
                continue
            if center == None and moved:
                break
            pa.click()
        return True

    def process_donation(self):
        logging.info("donate: Starting sequence...")
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
        