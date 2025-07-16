import cv2
import numpy as np
import time
from ultralytics import YOLO
from pathlib import Path

# 获取模型路径
src_dir = Path(__file__).parent.parent
model_path = src_dir / 'resources' / 'models' / 'best.pt'
output_dir = src_dir / "output"  # 输出目录

# 确保输出目录存在
output_dir.mkdir(parents=True, exist_ok=True)

# 加载模型（全局加载一次）
model = YOLO(str(model_path))

# 类别ID到名称的映射（使用下划线格式）
class_mapping = {
    0: "dark elixir drill",
    1: "elixir collector",
    2: "gold mine"
}

# 创建并保存classes.txt文件
def create_classes_txt():
    # 按照ID顺序获取类名列表
    class_names = [class_mapping[i] for i in sorted(class_mapping.keys())]
    
    # 创建classes.txt文件
    classes_path = output_dir / "classes.txt"
    with open(classes_path, 'w') as f:
        f.write("\n".join(class_names))

# 在首次导入时创建classes.txt
create_classes_txt()

class ObjectDetector:
    @staticmethod
    def detect_objects(screenshot, conf_threshold=0.4, save_annotated=False):
        """
        从截图中检测对象并保存结果用于Roboflow训练
        
        参数:
            screenshot: PIL截图对象
            conf_threshold: 置信度阈值
            save_annotated: 是否保存带检测框的可视化图片
            
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
        
        # 生成唯一文件名
        timestamp = int(time.time() * 1000)
        base_name = f"det_{timestamp}"
        
        # 保存原始图片（用于训练）
        raw_img_path = output_dir / f"{base_name}.png"
        cv2.imwrite(str(raw_img_path), screenshot_bgr)
        
        # 进行目标检测
        results = model.predict(
            source=screenshot_bgr,
            conf=conf_threshold,
            verbose=False,
            imgsz=640
        )
        
        # 解析检测结果
        detected_objects = []
        annotation_lines = []  # 存储YOLO格式标注
        
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
                
                # 保存原始类别ID（0,1,2）到标注文件
                annotation_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")
        
        # 保存YOLO标注文件（如有检测结果）
        if annotation_lines:
            annotation_path = output_dir / f"{base_name}.txt"
            with open(annotation_path, 'w') as f:
                f.write("\n".join(annotation_lines))
        
        # 可选：保存带检测框的可视化图片
        if save_annotated and results:
            annotated_img = results[0].plot()  # 获取带标注的图片
            annotated_path = output_dir / f"{base_name}_annotated.png"
            cv2.imwrite(str(annotated_path), annotated_img)
        
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
            actual_distance = raw_distance * 0.3 if obj['class_name'] == 'elixir collector' else raw_distance
            
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