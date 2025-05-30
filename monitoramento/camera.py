from datetime import datetime, timedelta
from pymongo import MongoClient
from .json_converter import from_dict
from .video_extractor import VideoFrameExtractor
from .object_detector import ObjectDetector
import cv2
import os

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
        self.last_detection_time = None
        self.detection_interval = timedelta(seconds=15)

    def generate_frames(self):
        """
        Gera frames do stream da câmera com as detecções em tempo real
        Mostra timestamp da última detecção
        """
        if not os.path.exists('frames'):
            os.makedirs('frames')
            
        cap = cv2.VideoCapture(self.url)
        
        if not cap.isOpened():
            raise Exception(f"Não foi possível conectar à câmera: {self.url}")
            
        while True:
            success, frame = cap.read()
            if not success:
                break
                
            # Processa o frame com o detector
            annotated_frame, detections = self.detector.process_image(frame)
            current_time = datetime.now()
            detected_objects = []
            
            # Processa as detecções
            if detections:
                for detection in detections:
                    class_name = detection['class_name']
                    confidence = detection['confidence']
                    detected_objects.append(f"{class_name} ({confidence:.2%})")
                
                # Verifica se passou tempo suficiente desde a última detecção
                if not self.last_detection_time or (current_time - self.last_detection_time) > self.detection_interval:
                    try:
                        detection_data = {
                            "camera_id": self.camera_id,
                            "timestamp": current_time,
                            "detections": detections
                        }
                        self.collection.insert_one(detection_data)
                        
                        frame_path = f"frames/detection_{current_time.strftime('%Y%m%d_%H%M%S')}.jpg"
                        cv2.imwrite(frame_path, annotated_frame)
                        print(f"Saved detection at {current_time}: {', '.join(detected_objects)}")
                        
                        self.last_detection_time = current_time
                        
                    except Exception as e:
                        print(f"Erro ao salvar detecção: {str(e)}")

            # Adiciona texto com timestamp e objetos detectados no frame
            if self.last_detection_time:
                timestamp_text = f"Ultima deteccao: {self.last_detection_time.strftime('%Y-%m-%d %H:%M:%S')}"
                cv2.putText(
                    annotated_frame,
                    timestamp_text,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA
                )
                
                if detected_objects:
                    objects_text = f"Objetos: {', '.join(detected_objects)}"
                    cv2.putText(
                        annotated_frame,
                        objects_text,
                        (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA
                    )

            # Stream do frame
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()