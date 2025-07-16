import logging
import cv2
import numpy as np
import pyautogui as pa
from pathlib import Path

class ImageLocator:
    def __init__(self):
        self.src_dir = Path(__file__).parent.parent
        self.images_dir = self.src_dir / 'resources' / 'images'
    
    def image_path(self, name):
        """获取图片完整路径"""
        name = name if name.endswith('.png') else f"{name}.png"
        path = self.images_dir / name
        if not path.exists():
            logging.warning(f"Image not found: {path}")
        return str(path.resolve())
    
    def locate_images(self, *image_names, confidence=0.8, color_sensitive=False, min_saturation=40):
        """定位图像，返回位置"""
        pa.sleep(0.3)
        for name in image_names:
            path = self.image_path(name)
            if not path:
                continue
                
            if not color_sensitive:
                try:
                    location = pa.locateOnScreen(path, confidence=confidence)
                    if location:
                        return location
                except:
                    continue
            else:
                screen = pa.screenshot()
                screen = np.array(screen)
                screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
                template = cv2.imread(path)
                if template is None:
                    continue
                
                screen_hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
                template_hsv = cv2.cvtColor(template, cv2.COLOR_BGR2HSV)
                res = cv2.matchTemplate(screen_hsv, template_hsv, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                
                if max_val >= confidence:
                    h, w = template.shape[:2]
                    left, top = max_loc
                    matched = screen_hsv[top:top+h, left:left+w]
                    if matched.shape[:2] == (h, w):
                        mean_s = matched[...,1].mean()
                        if mean_s >= min_saturation:
                            return (left, top, w, h)
        logging.debug(f"failed locate {name}")
        return None