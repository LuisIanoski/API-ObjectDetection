# API de Detecção de Objetos com YOLO

API Django para detecção de objetos em streams de vídeo usando YOLO e armazenamento SQLite.

## 🚀 Tecnologias

- Python 3.12+
- Django 5.2.1
- Django REST Framework
- SQLite3
- OpenCV
- YOLO (ultralytics)
- NumPy
- PyTorch

## 📋 Pré-requisitos

- Python 3.12 ou superior
- Ambiente virtual Python (venv)
- Git

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/LuisIanoski/API-ObjectDetection.git
cd API-ObjectDetection
```

2. Configure o ambiente virtual:
```bash
python -m venv nenv
nenv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py makemigrations camera monitoramento
python manage.py migrate
```

5. Crie um superusuário para acesso admin:
```bash
python manage.py createsuperuser
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

## 📁 Estrutura do Projeto

```
API-ObjectDetection/
├── camera/                 # App de gerenciamento de câmeras
│   ├── models.py          # Modelo de câmeras
│   ├── views.py           # ViewSets e lógica de negócio
│   ├── urls.py           # Rotas da API
│   └── services.py       # Serviços de processamento
├── monitoramento/         # App de detecções
│   ├── models.py         # Modelo de detecções
│   ├── views.py          # Views de stream e detecções
│   └── urls.py          # Rotas de monitoramento
├── extracaoimg/          # Configurações do projeto
└── frames/               # Frames salvos com detecções
```

## 🔒 Autenticação e Permissões

- Operações GET são públicas
- Operações POST, PUT, DELETE requerem autenticação admin
- Interface admin disponível em `/admin`

## 📡 Endpoints da API

### Câmeras (Camera)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/cameras/` | Lista câmeras | Não |
| POST | `/api/cameras/` | Adiciona câmera | Sim |
| GET | `/api/cameras/{id}/` | Detalhes da câmera | Não |
| PUT | `/api/cameras/{id}/` | Atualiza câmera | Sim |
| DELETE | `/api/cameras/{id}/` | Remove câmera | Sim |

### Monitoramento (Detection)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/cameras/{id}/stream/` | Stream ao vivo | Não |
| GET | `/api/cameras/{id}/detections/` | Lista detecções | Não |
| GET | `/api/detections/` | Todas detecções | Não |

## 📊 Modelos de Dados

### Camera
```python
{
    "camera_id": "string",     # Identificador único
    "camera_link": "string",   # URL do stream
    "camera_status": "string", # Status (active/inactive/error)
    "camera_loc": "string"     # Localização física
}
```

### Detection
```python
{
    "detection_id": "int",     # ID automático
    "detection_date": "date",  # Data (DD/MM/YY)
    "detection_time": "time",  # Hora (HH:MM)
    "detections": "array"      # Array de objetos detectados
}
```

## ⚙️ Configurações

- Intervalo entre detecções: 15 segundos (ajustável em `camera/services.py`)
- Confiança mínima: 0.45 (ajustável em `camera/object_detector.py`)
- Modelo YOLO: YOLO11s (configurável para outros modelos)
