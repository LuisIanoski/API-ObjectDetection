from ultralytics import YOLO
from typing import Union, Tuple, List
import numpy as np
import torch

class ObjectDetector:
    def __init__(self, model_path: str = "yolov8n.pt", confidence: float = 0.65):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.model.to('cuda' if torch.cuda.is_available() else 'cpu')

    def process_image(self, image: Union[str, np.ndarray]) -> Tuple[np.ndarray, List]:
        results = self.model(image, conf=self.confidence)
        return results[0].plot(), results[0].boxes.data.tolist()