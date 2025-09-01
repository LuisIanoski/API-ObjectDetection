const CAMERA_ID = 'CAM001'; // Ajuste para o ID da câmera desejada
const API_BASE_URL = '/api';

// Atualiza o horário atual
function updateCurrentTime() {
    const timeElement = document.getElementById('currentTime');
    const now = new Date();
    timeElement.textContent = now.toLocaleString();
}

// Atualiza o feed da câmera
function updateCameraFeed() {
    const cameraFeed = document.getElementById('cameraFeed');
    cameraFeed.src = `${API_BASE_URL}/stream/${CAMERA_ID}/`;
}

// Busca o status da câmera
async function updateCameraStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/cameras/${CAMERA_ID}/`);
        const data = await response.json();
        
        const statusElement = document.getElementById('cameraStatus');
        statusElement.textContent = data.camera_status;
        statusElement.className = `status-${data.camera_status.toLowerCase()}`;
    } catch (error) {
        console.error('Error fetching camera status:', error);
    }
}

// Busca as últimas detecções
async function updateDetections() {
    try {
        const response = await fetch(`${API_BASE_URL}/detections/${CAMERA_ID}/`);
        const data = await response.json();
        
        const detectionsBody = document.getElementById('detectionsBody');
        detectionsBody.innerHTML = '';

        // Pega as 10 últimas detecções
        const latestDetections = data.slice(0, 10);
        
        latestDetections.forEach(detection => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${new Date(detection.timestamp).toLocaleTimeString()}</td>
                <td>${detection.class_name}</td>
                <td>${(detection.confidence * 100).toFixed(1)}%</td>
            `;
            detectionsBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching detections:', error);
    }
}

// Inicialização e intervalos de atualização
document.addEventListener('DOMContentLoaded', () => {
    updateCurrentTime();
    updateCameraFeed();
    updateCameraStatus();
    updateDetections();

    // Atualiza o horário a cada segundo
    setInterval(updateCurrentTime, 1000);
    
    // Atualiza o status da câmera a cada 30 segundos
    setInterval(updateCameraStatus, 30000);
    
    // Atualiza as detecções a cada 5 segundos
    setInterval(updateDetections, 5000);
});