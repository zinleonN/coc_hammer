import logging
import asyncio
import time
import pyautogui as pa
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from common.image_utils import ImageLocator
from common.mouse_utils import MouseUtils
from tasks.attack import AttackManager
from tasks.donate import DonationManager


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 创建文件处理器
    log_file = Path(__file__).parent / 'app.log'
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    logging.info("Logging setup complete")

def main():
    setup_logging()
    idle_counter = 0
    MAX_IDLE_COUNT = 5
    sleep_time = 5

    attack = AttackManager()    
    donate = DonationManager()
    attack.execute_attack()

    while True:
        if donate.process_donation():
            logging.info("donated reset counter")
            idle_counter = 0
            sleep_time = 5
        else:
            idle_counter = idle_counter + 1

        if idle_counter == 0:
            logging.info("need resource")
            attack.execute_attack()
        if idle_counter >= MAX_IDLE_COUNT:
            logging.info(f"long time no donation needs, sleep for {sleep_time}s")
            time.sleep(sleep_time)
            idle_counter = 0
            if sleep_time <= 30: 
                sleep_time += 2    
            else:
                attack.execute_attack()
                sleep_time = 5

        

if __name__ == "__main__":
    main()