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


import logging
from pathlib import Path

def setup_logging():
    # 获取根 logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # 设置 logger 的最低级别为 DEBUG

    # 创建控制台 handler，设置级别为 INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建 formatter，并设置给 console handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)-6s - %(message)s')
    console_handler.setFormatter(formatter)

    # 添加 console handler 到 logger
    logger.addHandler(console_handler)

    # 创建文件 handler，设置级别为 DEBUG
    log_file = Path(__file__).parent / 'app.log'
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)-6s - %(message)s'))

    # 添加 file handler 到 logger
    logger.addHandler(file_handler)


def main():
    setup_logging()
    idle_counter = 0
    MAX_IDLE_COUNT = 5
    sleep_time = 5

    pa.hotkey('alt', 'tab')
    attack = AttackManager()    
    donate = DonationManager()
    attack.execute_attack()
    while True:
        if donate.process_donation():
            logging.info("main: donated reset counter")
            idle_counter = 0
            sleep_time = 5
        else:
            idle_counter = idle_counter + 1

        if idle_counter == 0:
            logging.info("main: need resource")
            attack.execute_attack()
        if idle_counter >= MAX_IDLE_COUNT:
            logging.info(f"main: long time no donation needs, sleep for {sleep_time}s")
            time.sleep(sleep_time)
            idle_counter = 0
            if sleep_time <= 30: 
                sleep_time += 2    
            else:
                attack.execute_attack()
                sleep_time = 5

        

if __name__ == "__main__":
    main()