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
    cameraFeed.src = `${API_BASE_URL}/cameras/${CAMERA_ID}/stream/`;
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
        const response = await fetch(`${API_BASE_URL}/cameras/${CAMERA_ID}/detections/`);
        const data = await response.json();
        
        const detectionsBody = document.getElementById('detectionsBody');
        detectionsBody.innerHTML = '';

        // Pega as 10 últimas detecções
        const latestDetections = Array.isArray(data) ? data.slice(0, 10) : [data];
        
        latestDetections.forEach(detection => {
            // Verifica se há detecções no array interno
            if (detection.detections && detection.detections.length > 0) {
                // Para cada objeto detectado neste frame
                detection.detections.forEach(obj => {
                    const row = document.createElement('tr');
                    const timestamp = `${detection.detection_date} ${detection.detection_time}`;
                    row.innerHTML = `
                        <td>${new Date(timestamp).toLocaleString('pt-BR')}</td>
                        <td>${obj.class_name}</td>
                        <td>${(obj.confidence * 100).toFixed(1)}%</td>
                    `;
                    detectionsBody.appendChild(row);
                });
            }
        });

        // Se não houver detecções, mostra mensagem
        if (detectionsBody.children.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="3" style="text-align: center;">Nenhuma detecção encontrada</td>';
            detectionsBody.appendChild(row);
        }
    } catch (error) {
        console.error('Error fetching detections:', error);
        const detectionsBody = document.getElementById('detectionsBody');
        detectionsBody.innerHTML = '<tr><td colspan="3" style="text-align: center; color: red;">Erro ao carregar detecções</td></tr>';
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