class DashboardManager {
    constructor() {
        this.API_BASE_URL = '/api/dashboards';
        this.initializeEventListeners();
        this.loadDashboards();
    }

    initializeEventListeners() {
        // Form para criar dashboard
        document.getElementById('dashboardForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.createDashboard();
        });

        // Form para adicionar câmera
        document.getElementById('cameraForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addCamera();
        });
    }

    async createDashboard() {
        const data = {
            dashboard_id: document.getElementById('dashboardId').value,
            name: document.getElementById('dashboardName').value,
            risco: document.getElementById('dashboardRisco').value
        };

        try {
            const response = await fetch(this.API_BASE_URL + '/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error('Erro ao criar dashboard');
            
            this.showMessage('Dashboard criado com sucesso!', 'success');
            this.loadDashboards();
            document.getElementById('dashboardForm').reset();
        } catch (error) {
            this.showMessage(error.message, 'error');
        }
    }

    async addCamera() {
        const dashboardId = document.getElementById('dashboardSelect').value;
        const data = {
            camera_id: document.getElementById('cameraId').value,
            camera_link: document.getElementById('cameraLink').value,
            camera_loc: document.getElementById('cameraLoc').value,
            camera_status: document.getElementById('cameraStatus').value
        };

        try {
            const response = await fetch(`${this.API_BASE_URL}/${dashboardId}/add-camera/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error('Erro ao adicionar câmera');
            
            this.showMessage('Câmera adicionada com sucesso!', 'success');
            this.loadDashboards();
            document.getElementById('cameraForm').reset();
        } catch (error) {
            this.showMessage(error.message, 'error');
        }
    }

    async loadDashboards() {
        try {
            const response = await fetch(this.API_BASE_URL + '/');
            const dashboards = await response.json();
            
            this.updateDashboardsList(dashboards);
            this.updateDashboardSelect(dashboards);
        } catch (error) {
            this.showMessage('Erro ao carregar dashboards', 'error');
        }
    }

    updateDashboardsList(dashboards) {
        const container = document.getElementById('dashboardsList');
        container.innerHTML = '';

        dashboards.forEach(dashboard => {
            const card = document.createElement('div');
            card.className = 'dashboard-card';
            card.innerHTML = `
                <h3>${dashboard.name} (${dashboard.dashboard_id})</h3>
                <div class="camera-list">
                    <h4>Câmeras:</h4>
                    ${this.renderCameraList(dashboard.cameras)}
                </div>
            `;
            container.appendChild(card);
        });
    }

    renderCameraList(cameras) {
        if (!cameras || cameras.length === 0) {
            return '<p>Nenhuma câmera cadastrada</p>';
        }

        return `
            <ul>
                ${cameras.map(camera => `
                    <li>
                        ${camera.camera_id} - ${camera.camera_loc}
                        (${camera.camera_status})
                    </li>
                `).join('')}
            </ul>
        `;
    }

    updateDashboardSelect(dashboards) {
        const select = document.getElementById('dashboardSelect');
        select.innerHTML = '<option value="">Selecione um Dashboard</option>';
        
        dashboards.forEach(dashboard => {
            const option = document.createElement('option');
            option.value = dashboard.dashboard_id;
            option.textContent = `${dashboard.name} (${dashboard.dashboard_id})`;
            select.appendChild(option);
        });
    }

    showMessage(message, type) {
        const div = document.createElement('div');
        div.className = type;
        div.textContent = message;
        
        document.querySelector('.container').insertAdjacentElement('afterbegin', div);
        
        setTimeout(() => div.remove(), 3000);
    }
}

// Inicializa o gerenciador
new DashboardManager();