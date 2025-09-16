const API_BASE_URL = '/api';
let CAMERA_ID = null;

// Função para inicializar o dashboard
function initializeDashboard() {
    console.log('Inicializando Chirp Dashboard...');
    
    if (window.INITIAL_DATA && window.INITIAL_DATA.cameras && window.INITIAL_DATA.cameras.length > 0) {
        const cameras = window.INITIAL_DATA.cameras;
        CAMERA_ID = cameras[0].id;
        
        const select = document.getElementById('cameraSelect');
        if (select) {
            select.value = CAMERA_ID;
            console.log('Câmera inicial selecionada:', CAMERA_ID);
            updateDashboard();
        }
    } else {
        const select = document.getElementById('cameraSelect');
        if (select && select.options.length > 1) {
            for (let i = 1; i < select.options.length; i++) {
                if (select.options[i].value) {
                    CAMERA_ID = select.options[i].value;
                    select.value = CAMERA_ID;
                    console.log('Câmera selecionada via select:', CAMERA_ID);
                    updateDashboard();
                    break;
                }
            }
        }
    }
}

// Atualizar data e hora
function updateDateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('pt-BR', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    const dateString = now.toLocaleDateString('pt-BR', { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric' 
    });
    
    const dateTimeElement = document.getElementById('currentDateTime');
    if (dateTimeElement) {
        dateTimeElement.textContent = `${timeString} - ${dateString}`;
    }
}

// Atualizar feed da câmera
function updateCameraFeed() {
    const cameraFeed = document.getElementById('cameraFeed');
    const videoContainer = document.getElementById('videoContainer');
    
    if (!CAMERA_ID) {
        showVideoPlaceholder();
        return;
    }
    
    if (cameraFeed && videoContainer) {
        const timestamp = new Date().getTime();
        const streamUrl = `${API_BASE_URL}/cameras/${CAMERA_ID}/stream/?t=${timestamp}`;
        
        cameraFeed.src = streamUrl;
        cameraFeed.style.display = 'block';
        
        // Esconder placeholder
        const placeholder = videoContainer.querySelector('.video-placeholder');
        if (placeholder) {
            placeholder.style.display = 'none';
        }
        
        // Tratamento de erro de carregamento
        cameraFeed.onerror = () => {
            showVideoPlaceholder();
        };
        
        console.log('Feed da câmera atualizado:', streamUrl);
    }
}

// Mostrar placeholder do vídeo
function showVideoPlaceholder() {
    const cameraFeed = document.getElementById('cameraFeed');
    const videoContainer = document.getElementById('videoContainer');
    
    if (cameraFeed) {
        cameraFeed.style.display = 'none';
    }
    
    if (videoContainer) {
        const placeholder = videoContainer.querySelector('.video-placeholder');
        if (placeholder) {
            placeholder.style.display = 'block';
        }
    }
}

// Atualizar status da câmera
async function updateCameraStatus() {
    if (!CAMERA_ID) {
        const statusElement = document.getElementById('cameraStatus');
        if (statusElement) {
            statusElement.textContent = 'Status';
        }
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/cameras/${CAMERA_ID}/`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const data = await response.json();
        const statusElement = document.getElementById('cameraStatus');
        
        if (statusElement) {
            statusElement.textContent = data.camera_status || 'Desconhecido';
            
            // Atualizar cor do status dot
            const statusDot = document.querySelector('.status-dot');
            if (statusDot) {
                if (data.camera_status === 'active') {
                    statusDot.style.background = '#10b981'; // Verde
                } else if (data.camera_status === 'error') {
                    statusDot.style.background = '#ef4444'; // Vermelho
                } else {
                    statusDot.style.background = '#f59e0b'; // Amarelo
                }
            }
        }
        
        // Atualizar localização
        const locationElement = document.getElementById('locationName');
        if (locationElement && data.camera_loc) {
            locationElement.textContent = data.camera_loc;
        }
        
    } catch (error) {
        console.error('Erro ao buscar status da câmera:', error);
        const statusElement = document.getElementById('cameraStatus');
        if (statusElement) {
            statusElement.textContent = 'Erro';
        }
    }
}

// Atualizar detecções
async function updateDetections() {
    if (!CAMERA_ID) {
        const detectionsBody = document.getElementById('detectionsBody');
        if (detectionsBody) {
            detectionsBody.innerHTML = '<tr><td colspan="3" style="text-align: center;">Selecione uma câmera</td></tr>';
        }
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/cameras/${CAMERA_ID}/detections/`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const data = await response.json();
        const detectionsBody = document.getElementById('detectionsBody');
        
        if (!detectionsBody) return;

        detectionsBody.innerHTML = '';
        
        const latestDetections = Array.isArray(data) ? data.slice(0, 10) : [];
        
        if (latestDetections.length > 0) {
            latestDetections.forEach(detection => {
                if (detection.detections && detection.detections.length > 0) {
                    detection.detections.forEach(obj => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${detection.detection_date}</td>
                            <td>${obj.class_name}</td>
                            <td>${detection.detection_time}</td>
                        `;
                        detectionsBody.appendChild(row);
                    });
                }
            });
        }

        if (detectionsBody.children.length === 0) {
            detectionsBody.innerHTML = '<tr><td colspan="3" style="text-align: center;">Nenhuma detecção encontrada</td></tr>';
        }
    } catch (error) {
        console.error('Erro ao buscar detecções:', error);
        const detectionsBody = document.getElementById('detectionsBody');
        if (detectionsBody) {
            detectionsBody.innerHTML = '<tr><td colspan="3" style="text-align: center; color: #ef4444;">Erro ao carregar</td></tr>';
        }
    }
}

// Simular dados de clima (pode ser integrado com API real)
function updateWeatherInfo() {
    const days = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
    const today = new Date().getDay();
    const weatherSection = document.querySelector('.weather-section h3');
    
    if (weatherSection) {
        weatherSection.textContent = days[today];
    }
}

// Atualizar informações de risco (pode ser customizado conforme necessidade)
function updateRiskInfo() {
    // Esta função pode ser expandida para calcular risco real baseado nas detecções
    const riskLevel = document.getElementById('riskLevel');
    const riskDescription = document.getElementById('riskDescription');
    
    if (riskLevel) {
        // Exemplo de lógica de risco - pode ser customizada
        riskLevel.textContent = 'Baixo';
        riskLevel.style.color = '#10b981';
    }
    
    if (riskDescription) {
        riskDescription.textContent = 'Nível normal';
    }
}

// Função principal para atualizar todo o dashboard
function updateDashboard() {
    if (!CAMERA_ID) {
        console.log('Nenhuma câmera selecionada');
        return;
    }
    
    console.log('Atualizando dashboard para câmera:', CAMERA_ID);
    updateCameraFeed();
    updateCameraStatus();
    updateDetections();
    updateRiskInfo();
}

// Configurar event listener do select de câmera
function setupCameraSelectListener() {
    const cameraSelect = document.getElementById('cameraSelect');
    if (cameraSelect) {
        cameraSelect.addEventListener('change', function(event) {
            const selectedValue = event.target.value;
            console.log('Câmera selecionada:', selectedValue);
            
            if (selectedValue && selectedValue !== '') {
                CAMERA_ID = selectedValue;
                updateDashboard();
            } else {
                CAMERA_ID = null;
                showVideoPlaceholder();
                
                // Limpar informações
                const statusElement = document.getElementById('cameraStatus');
                if (statusElement) statusElement.textContent = 'Status';
                
                const locationElement = document.getElementById('locationName');
                if (locationElement) locationElement.textContent = 'Cdd, Estd, País';
            }
        });
        console.log('Event listener do select configurado');
    }
}

// Inicialização quando DOM carregar
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM carregado, inicializando Chirp Dashboard...');
    
    // Configurar listeners
    setupCameraSelectListener();
    
    // Inicializar dashboard
    initializeDashboard();
    
    // Configurar atualizações de tempo
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Configurar informações estáticas
    updateWeatherInfo();
    
    // Configurar intervalos de atualização
    if (CAMERA_ID) {
        updateCameraStatus();
        updateDetections();
    }
    
    // Atualizar dados automaticamente
    setInterval(() => {
        if (CAMERA_ID) {
            updateCameraStatus();
            updateDetections();
        }
    }, 5000);
});

// Funções utilitárias para debug
function debugDashboard() {
    console.log('=== CHIRP DASHBOARD DEBUG ===');
    console.log('CAMERA_ID:', CAMERA_ID);
    console.log('INITIAL_DATA:', window.INITIAL_DATA);
    console.log('Select value:', document.getElementById('cameraSelect')?.value);
    console.log('============================');
}

// Função para forçar atualização
function forceUpdate() {
    if (CAMERA_ID) {
        console.log('Forçando atualização...');
        updateDashboard();
    }
}