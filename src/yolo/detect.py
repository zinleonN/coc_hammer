import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path

# 获取模型路径
src_dir = Path(__file__).parent.parent
model_path = src_dir / 'resources' / 'models' / 'best.pt'

# 加载模型（全局加载一次）
model = YOLO(str(model_path))

class ObjectDetector:
    @staticmethod
    def detect_objects(screenshot, conf_threshold=0.4):
        """
        从截图中检测对象
        
        参数:
            screenshot: PIL截图对象
            conf_threshold: 置信度阈值
            
        返回:
            检测到的对象列表，每个对象包含:
                class_name: 类别名称
                confidence: 置信度
                bbox: [x1, y1, x2, y2] 边界框
                center: [cx, cy] 中心点坐标
        """
        screenshot_np = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
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
                class_name = result.names[class_id]
                confidence = box.conf.item()
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # 添加到结果列表
                detected_objects.append({
                    "class_name": class_name,
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2],
                    "center": [(x1 + x2) / 2, (y1 + y2) / 2]
                })
        
        return detected_objects

    @staticmethod
    def calculate_avg_distance_to_line(k, x0, y0, screenshot):
        """
        计算所有检测点到直线的平均距离，并返回小于平均距离的点在直线上的映射点
        
        参数:
            k: 直线斜率
            x0, y0: 直线经过的点坐标
            screenshot: PIL截图对象
            
        返回:
            tuple: (平均距离, 映射点列表) 
                    映射点列表包含所有距离小于平均距离的点在直线上的投影坐标 (x_proj, y_proj)
        """
        # 计算直线截距 (y = kx + b)
        b = y0 - k * x0
        
        # 检测对象
        detected_objects = ObjectDetector.detect_objects(screenshot)
        
        if not detected_objects:
            return float('inf'), []
        
        total_distance = 0
        projected_points = []  # 存储所有投影点坐标
        distances = []  # 存储所有点的距离

        # 处理每个检测到的对象
        for obj in detected_objects:
            cx, cy = obj['center']
            
            # 计算点到直线的原始距离: |kx - y + b|/√(k²+1)
            numerator = abs(k * cx - cy + b)
            denominator = np.sqrt(k**2 + 1)
            raw_distance = numerator / denominator
            
            # 应用类别权重
            actual_distance = raw_distance * 0.5 if obj['class_name'] == 'elixir collector' else raw_distance
            
            # 计算映射点（垂足）
            # 使用向量投影公式计算垂足坐标
            if abs(k) < 1e5:  # 处理非垂直线
                x_proj = (cx + k * (cy - b)) / (k**2 + 1)
                y_proj = k * x_proj + b
            else:  # 处理垂直线（k无穷大）
                x_proj = x0
                y_proj = cy
            
            # 存储投影点和距离
            projected_points.append((x_proj, y_proj))
            distances.append(actual_distance)
            total_distance += actual_distance

        # 计算平均距离
        avg_distance = total_distance / len(distances)
        
        # 筛选小于平均距离的投影点
        below_avg_projected_points = [
            projected_points[i] 
            for i in range(len(distances)) 
            if distances[i] < avg_distance
        ]
        
        return avg_distance, below_avg_projected_points