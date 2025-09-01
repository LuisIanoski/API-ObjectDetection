from datetime import datetime, timedelta
from camera.models import Camera, Detection
from .object_detector import ObjectDetector
import cv2
import os

class Camera:
    def __init__(self, camera_id: str, url: str = None):
        """
        Inicializa uma câmera para monitoramento
        Args:
            camera_id: Identificador único da câmera
            url: URL da câmera
        """
        try:
            self.camera = Camera.objects.get(camera_id=camera_id)
            self.url = url or self.camera.camera_link
            self.detector = ObjectDetector()
            self.last_detection_time = None
            self.detection_interval = timedelta(seconds=15)
        except Camera.DoesNotExist:
            raise ValueError(f"Camera {camera_id} not found")

    def get_detections(self, date: str = None):
        """
        Recupera as detecções usando Django ORM
        Args:
            date: Data opcional para filtrar (formato: YYYY-MM-DD)
        Returns:
            Lista de detecções
        """
        queryset = Detection.objects.filter(camera=self.camera)
        
        if date:
            start_date = datetime.strptime(date, '%Y-%m-%d')
            end_date = start_date + timedelta(days=1)
            queryset = queryset.filter(timestamp__date=start_date)
            
        return queryset
    
    def generate_frames(self):
        """
        Gera frames do stream da câmera com as detecções em tempo real
        """
        if not os.path.exists('frames'):
            os.makedirs('frames')
            
        cap = cv2.VideoCapture(self.url)
        
        if not cap.isOpened():
            self.camera.camera_status = 'error'
            self.camera.save()
            raise Exception(f"Não foi possível conectar à câmera: {self.url}")
            
        while True:
            success, frame = cap.read()
            if not success:
                break
                
            annotated_frame, detections = self.detector.process_image(frame)
            current_time = datetime.now()
            detected_objects = []
            
            if detections:
                for detection in detections:
                    class_name = detection['class_name']
                    confidence = detection['confidence']
                    detected_objects.append(f"{class_name} ({confidence:.2%})")
                
                if not self.last_detection_time or (current_time - self.last_detection_time) > self.detection_interval:
                    try:
                        for detection in detections:
                            Detection.objects.create(
                                camera=self.camera,
                                timestamp=current_time,
                                class_name=detection['class_name'],
                                confidence=detection['confidence'],
                                bbox_x=detection['bbox'][0],
                                bbox_y=detection['bbox'][1],
                                bbox_width=detection['bbox'][2],
                                bbox_height=detection['bbox'][3]
                            )
                        
                        frame_path = f"frames/detection_{current_time.strftime('%Y%m%d_%H%M%S')}.jpg"
                        cv2.imwrite(frame_path, annotated_frame)
                        print(f"Saved detection at {current_time}: {', '.join(detected_objects)}")
                        
                        self.last_detection_time = current_time
                        
                    except Exception as e:
                        print(f"Erro ao salvar detecção: {str(e)}")

            if self.last_detection_time:
                timestamp_text = f"Ultima deteccao: {self.last_detection_time.strftime('%Y-%m-%d %H:%M:%S')}"
                location_text = f"Local: {self.camera.camera_loc}"
                
                cv2.putText(annotated_frame, timestamp_text, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(annotated_frame, location_text, (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                
                if detected_objects:
                    objects_text = f"Objetos: {', '.join(detected_objects)}"
                    cv2.putText(annotated_frame, objects_text, (10, 110),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()
