from datetime import datetime, timedelta
import cv2
import os
from .models import Camera
from monitoramento.models import Detection
from .object_detector import ObjectDetector

class CameraService:
    def __init__(self, camera_id: str):
        try:
            self.camera = Camera.objects.get(camera_id=camera_id)
            self.detector = ObjectDetector()
            self.last_detection_time = None
            self.detection_interval = timedelta(seconds=15)
        except Camera.DoesNotExist:
            raise ValueError(f"Camera {camera_id} not found")

    def generate_frames(self):
        """Gera frames do stream da câmera com as detecções em tempo real"""
        if not os.path.exists('frames'):
            os.makedirs('frames')
            
        cap = cv2.VideoCapture(self.camera.camera_link)
        
        if not cap.isOpened():
            self.camera.camera_status = 'error: cannot connect'
            self.camera.save()
            raise Exception(f"Não foi possível conectar à câmera: {self.camera.camera_link}")
            
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
                
                if not self.last_detection_time or \
                   (current_time - self.last_detection_time) > self.detection_interval:
                    try:
                        # Save detection to database
                        Detection.objects.create(
                            camera=self.camera,
                            detection_date=current_time.date(),
                            detection_time=current_time.time(),
                            detections=detections
                        )
                        
                        # Save frame
                        frame_path = f"frames/detection_{current_time.strftime('%Y%m%d_%H%M%S')}.jpg"
                        cv2.imwrite(frame_path, annotated_frame)
                        print(f"Saved detection at {current_time}: {', '.join(detected_objects)}")
                        
                        self.last_detection_time = current_time
                        
                    except Exception as e:
                        print(f"Erro ao salvar detecção: {str(e)}")

            # Add overlay text
            if self.last_detection_time:
                timestamp_text = f"Ultima deteccao: {self.last_detection_time.strftime('%d/%m/%y %H:%M')}"
                location_text = f"Local: {self.camera.camera_loc}"
                
                cv2.putText(annotated_frame, timestamp_text, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(annotated_frame, location_text, (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()