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
    attack = AttackManager()
    attack.execute_attack()

if __name__ == "__main__":
    main()