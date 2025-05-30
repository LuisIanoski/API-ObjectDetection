from ultralytics import YOLO
from typing import Union, Tuple, List, Dict
import numpy as np
import torch

class ObjectDetector:
    def __init__(self, model_path: str = "yolov8n.pt", confidence: float = 0.45):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.model.to('cuda' if torch.cuda.is_available() else 'cpu')

    def process_image(self, image: Union[str, np.ndarray]) -> Tuple[np.ndarray, List[Dict]]:
        results = self.model(image, conf=self.confidence)
        
        # Create list of detections with class names
        detections = []
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            class_name = results[0].names[class_id]
            confidence = float(box.conf[0])
            bbox = box.xyxy[0].tolist()
            
            detections.append({
                'class_id': class_id,
                'class_name': class_name,
                'confidence': confidence,
                'bbox': bbox
            })
            
        return results[0].plot(), detections