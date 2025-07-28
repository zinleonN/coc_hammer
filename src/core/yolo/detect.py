import cv2
import numpy as np
import time
import shutil
from ultralytics import YOLO
from pathlib import Path

from core.common.file import resource_path

model = YOLO(resource_path("best.pt"))

class_mapping = {
    0: "dark elixir drill",
    1: "elixir collector",
    2: "gold mine"
}

def detect_objects(screenshot, conf_threshold=0.5):
    """
    从截图中检测对象并保存结果用于Roboflow训练
    
    参数:
        screenshot: PIL截图对象
        conf_threshold: 置信度阈值
        
    返回:
        检测到的对象列表，每个对象包含:
            class_name: 类别名称（下划线格式）
            confidence: 置信度
            bbox: [x1, y1, x2, y2] 边界框
            center: [cx, cy] 中心点坐标
    """
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    height, width = screenshot_bgr.shape[:2]
    
    
    # 进行目标检测
    results = model.predict(
        source=screenshot_bgr,
        conf=conf_threshold,
        verbose=False,
        imgsz=640
    )
    
    # 解析检测结果
    detected_objects = []
    
    if results:
        result = results[0]
        for box in result.boxes:
            # 获取检测信息
            class_id = int(box.cls)
            class_name = class_mapping.get(class_id, f"unknown_{class_id}")
            confidence = box.conf.item()
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            
            # 添加到结果列表
            detected_objects.append({
                "class_name": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2],
                "center": [(x1 + x2) / 2, (y1 + y2) / 2]
            })
            
            # 转换为YOLO格式：归一化的中心坐标和宽高
            x_center = (x1 + x2) / 2 / width
            y_center = (y1 + y2) / 2 / height
            w = (x2 - x1) / width
            h = (y2 - y1) / height
            
    return detected_objects