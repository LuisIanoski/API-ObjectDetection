const API_BASE_URL = '/api/monitoramento';  // Updated to match existing URL structure
let CAMERA_ID = null;

function initializeDashboard() {
    const { cameras } = window.INITIAL_DATA;
    
    if (cameras && cameras.length > 0) {
        const select = document.getElementById('cameraSelect');
        if (select) {
            CAMERA_ID = cameras[0].id;
            select.value = CAMERA_ID;
            console.log('Initialized camera:', CAMERA_ID);
            updateDashboard();
        }
    }
}

function updateCurrentTime() {
    const timeElement = document.getElementById('currentTime');
    if (timeElement) {
        timeElement.textContent = new Date().toLocaleString('pt-BR');
    }
}

function updateCameraFeed() {
    const cameraFeed = document.getElementById('cameraFeed');
    if (cameraFeed && CAMERA_ID) {
        const timestamp = new Date().getTime();
        cameraFeed.src = `${API_BASE_URL}/camera/stream/${CAMERA_ID}/?t=${timestamp}`;
    }
}

async function updateCameraStatus() {
    const statusElement = document.getElementById('cameraStatus');
    
    if (!CAMERA_ID || !statusElement) {
        console.log('Cannot update status: No camera selected or status element not found');
        return;
    }

    try {
        console.log('Fetching status for camera:', CAMERA_ID);
        const response = await fetch(`${API_BASE_URL}/camera/status/${CAMERA_ID}/`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const data = await response.json();
        console.log('Camera status:', data);
        
        statusElement.textContent = data.status || 'Desconhecido';
        statusElement.className = `status-${(data.status || 'unknown').toLowerCase()}`;
    } catch (error) {
        console.error('Error fetching camera status:', error);
        statusElement.textContent = 'Erro ao carregar status';
        statusElement.className = 'status-error';
    }
}

async function updateDetections() {
    if (!CAMERA_ID) return;

    try {
        const response = await fetch(`${API_BASE_URL}/camera/detections/${CAMERA_ID}/`);
        const data = await response.json();
        
        const detectionsBody = document.getElementById('detectionsBody');
        if (!detectionsBody) return;

        detectionsBody.innerHTML = '';
        
        const latestDetections = Array.isArray(data) ? data.slice(0, 10) : [data];
        
        latestDetections.forEach(detection => {
            if (detection.detections?.length > 0) {
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

        if (detectionsBody.children.length === 0) {
            detectionsBody.innerHTML = '<tr><td colspan="3" style="text-align: center;">Nenhuma detecção encontrada</td></tr>';
        }
    } catch (error) {
        console.error('Error fetching detections:', error);
        const detectionsBody = document.getElementById('detectionsBody');
        if (detectionsBody) {
            detectionsBody.innerHTML = '<tr><td colspan="3" style="text-align: center; color: red;">Erro ao carregar detecções</td></tr>';
        }
    }
}

function updateDashboard() {
    if (!CAMERA_ID) return;
    updateCameraFeed();
    updateCameraStatus();
    updateDetections();
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing dashboard...');
    initializeDashboard();
    updateCurrentTime();

    // Set up event listeners
    const cameraSelect = document.getElementById('cameraSelect');
    if (cameraSelect) {
        cameraSelect.addEventListener('change', (e) => {
            CAMERA_ID = e.target.value;
            console.log('Camera changed to:', CAMERA_ID);
            updateDashboard();
        });
    }

    // Set up intervals with immediate first call
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);

    // Update camera status and detections
    if (CAMERA_ID) {
        updateCameraStatus();
        updateDetections();
    }

    // Set shorter interval for critical updates
    setInterval(() => {
        if (CAMERA_ID) {
            updateCameraStatus();
            updateDetections();
        }
    }, 3000); // Update every 3 seconds instead of 5
});

// Add a helper function to force update
function forceUpdate() {
    if (CAMERA_ID) {
        console.log('Forcing update for camera:', CAMERA_ID);
        updateCameraStatus();
        updateDetections();
    }
}