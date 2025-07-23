import sys
import os
from pathlib import Path

def path_locate(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent / "resources"
    
    return str(base_path / relative_path)

def image_path(name):
    if not name.lower().endswith('.png'):
        name = f"{name}.png"
    path = path_locate(f"images/{name}")
    
    if not Path(path).exists():
        raise FileNotFoundError(f"图片文件不存在: {path}")
    
    return path

def resource_path(name):
    path = path_locate(name)

    if not Path(path).exists():
        raise FileNotFoundError(f"文件不存在: {path}")
    
    return path
