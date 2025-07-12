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

def main():
    attack = AttackManager()
    attack.execute_attack()

if __name__ == "__main__":
    main()