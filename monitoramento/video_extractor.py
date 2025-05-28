from .object_detector import ObjectDetector
import cv2
import time
import os
import shutil
import subprocess
import datetime

class VideoFrameExtractor:
    def __init__(self, stream_url, output_dir="frames", capture_interval=5):
        """
        Inicializa o extrator de frames
        :param stream_url: URL do stream de vídeo
        :param output_dir: Diretório para salvar os frames
        :param capture_interval: Intervalo entre capturas em segundos
        """
        self.stream_url = stream_url
        self.output_dir = output_dir
        self.capture_interval = capture_interval
        self._setup_output_dir()

    def _setup_output_dir(self):
        """Cria o diretório de saída se não existir"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def capture_frame(self):
        """
        Captura um único frame do stream
        :return: Caminho do arquivo salvo ou None em caso de erro
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"frame_{timestamp}.jpg")
        
        command = [
            'ffmpeg',
            '-y',
            '-i', self.stream_url,
            '-vframes', '1',
            '-f', 'image2',
            output_file
        ]
        
        try:
            subprocess.run(command, check=True, capture_output=True)
            print(f"Frame capturado com sucesso: {output_file}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"Erro ao capturar frame: {e}")
            return None

    def start_capture(self):
        """Inicia o loop de captura de frames"""
        detector = ObjectDetector()
        print(f"Iniciando captura de frames de {self.stream_url}")
        try:
            while True:
                frame_path = self.capture_frame()
                if frame_path:
                    # Processa o frame capturado
                    annotated_frame, detections = detector.process_image(frame_path)
                    # Opcional: salvar frame processado
                    cv2.imwrite(frame_path.replace('.jpg', '_processed.jpg'), annotated_frame)
                    print("Detecções encontradas:")
                    for det in detections:
                        print(f"Classe: {det['class_name']}, Confiança: {det['confidence']:.2f}")
                time.sleep(self.capture_interval)
        except KeyboardInterrupt:
            print("\nCaptura de frames interrompida pelo usuário")