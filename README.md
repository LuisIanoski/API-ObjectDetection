# API de Detecção de Objetos

API Django para detecção de objetos em streams de vídeo usando YOLO.

## Requisitos

- Python 3.12+
- Django 5.2.1
- OpenCV
- PyMongo
- YOLO (ultralytics)

## Instalação

1. Clone o repositório
```bash
git clone (https://github.com/LuisIanoski/API-ObjectDetection.git)
cd API-extração-img
```

2. Crie e ative o ambiente virtual
```bash
python -m venv nenv
nenv\Scripts\activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Execute as migrações
```bash
python manage.py migrate
```

5. Inicie o servidor
```bash
python manage.py runserver
```

## Endpoints

- `GET /api/cameras/<camera_id>/stream/`: Stream ao vivo com detecções
- `GET /api/cameras/<camera_id>/detections/`: Lista de detecções

## Configuração

Configure a URL da câmera em `monitoramento/views.py`.
