from datetime import datetime
from pymongo import MongoClient
from .json_converter import from_dict
from .video_extractor import VideoFrameExtractor
from .object_detector import ObjectDetector
import cv2

class Camera:
    def __init__(self, camera_id: str, url: str = None, db_uri: str = "mongodb://localhost:27017/"):
        """
        Inicializa uma câmera para monitoramento
        Args:
            camera_id: Identificador único da câmera
            db_uri: URI de conexão com MongoDB
        """
        self.camera_id = camera_id
        self.url = url
        self.db_client = MongoClient(db_uri)
        self.db = self.db_client.camera_monitoring
        self.collection = self.db.detections
        self.detector = ObjectDetector()

    def get_detections(self, date: str = None):
        """
        Recupera detecções da câmera
        Args:
            date: Data no formato dd/mm/yy (opcional)
        Returns:
            Lista de detecções
        """
        query = {"camera_id": self.camera_id}
        if date:
            query["date"] = date
        
        return list(self.collection.find(query, {"_id": 0}))

    def generate_frames(self):
        """
        Gera frames do stream da câmera com as detecções em tempo real
        """
        cap = cv2.VideoCapture(self.url)
        
        if not cap.isOpened():
            raise Exception(f"Não foi possível conectar à câmera: {self.url}")
            
        while True:
            success, frame = cap.read()
            if not success:
                break
                
            # Processa o frame com o detector
            annotated_frame, detections = self.detector.process_image(frame)
            
            # Salva as detecções no MongoDB
            if detections:
                detection_data = {
                    "camera_id": self.camera_id,
                    "timestamp": datetime.now(),
                    "detections": detections
                }
                self.collection.insert_one(detection_data)

            # Converte o frame para jpg
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()
            
            # Retorna o frame no formato multipart
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()