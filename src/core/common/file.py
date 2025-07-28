import sys
import os
import json
from pathlib import Path

from core.common.log import get_logger

logger = get_logger()

def path_locate(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent.parent / "resources"
    
    return str(base_path / relative_path)

def image_path(name):
    if not name.lower().endswith('.png'):
        name = f"{name}.png"
    path = path_locate(f"images/{name}")
    
    if not Path(path).exists():
        logger.error(f"image not found in: {path}")
        exit(-1)
    return path

def resource_path(name):
    path = path_locate(name)
    logger.debug(f"resource path: {path}")
    if not Path(path).exists():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        logger.debug("resource not exist, creating empty file")
    return path

def load_settings():
    try:
        with open(resource_path("settings.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.debug(e)
        return {}
    
def save_settings(settings: dict):
    try:
        with open(resource_path("settings.json"), "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.debug(e)