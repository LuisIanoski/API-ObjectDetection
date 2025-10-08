class RiskManager {
    constructor(dashboardId) {
        this.dashboardId = dashboardId;
        this.API_BASE_URL = '/api/dashboards';
        this.currentRisk = null;
        this.riskLevels = [];

        this.init();
    }

    async init() {
        await this.loadRiskLevels();
        await this.loadCurrentRisk();
        this.updateInterface();
        this.setupEventListeners();
        this.setupDateTime();
    }

    async loadRiskLevels() {
        try {
            const response = await fetch(`${this.API_BASE_URL}/risk-levels/`);
            if (!response.ok) throw new Error('Erro ao carregar níveis de risco');

            const data = await response.json();
            this.riskLevels = data.risk_levels;
            console.log('Níveis de risco carregados:', this.riskLevels);
        } catch (error) {
            console.error('Erro ao carregar níveis de risco:', error);
            this.showNotification('Erro ao carregar níveis de risco', 'error');

            // Fallback com dados padrão
            this.riskLevels = [
                { value: 'baixo', display: 'Baixo', color: '#10b981' },
                { value: 'medio', display: 'Médio', color: '#f59e0b' },
                { value: 'alto', display: 'Alto', color: '#ef4444' },
                { value: 'critico', display: 'Crítico', color: '#dc2626' }
            ];
        }
    }

    async loadCurrentRisk() {
        try {
            const response = await fetch(`${this.API_BASE_URL}/${this.dashboardId}/`);
            if (!response.ok) throw new Error('Erro ao carregar dashboard');

            const data = await response.json();
            this.currentRisk = {
                value: data.risco,
                display: data.risco_display,
                color: data.risco_color,
                updated_at: data.updated_at || new Date().toISOString()
            };

            console.log('Risco atual:', this.currentRisk);
        } catch (error) {
            console.error('Erro ao carregar risco atual:', error);

            // Fallback com dados iniciais
            this.currentRisk = {
                value: window.INITIAL_DATA.dashboard_risco,
                display: window.INITIAL_DATA.dashboard_risco_display,
                color: window.INITIAL_DATA.dashboard_risco_color,
                updated_at: new Date().toISOString()
            };
        }
    }

    updateInterface() {
        // Atualizar indicador de risco
        const riskIndicator = document.getElementById('riskIndicator');
        if (riskIndicator && this.currentRisk) {
            riskIndicator.style.backgroundColor = this.currentRisk.color;
        }

        // Atualizar badge de risco atual
        const currentRiskBadge = document.getElementById('currentRiskBadge');
        if (currentRiskBadge && this.currentRisk) {
            currentRiskBadge.textContent = this.currentRisk.display;
            currentRiskBadge.style.color = this.currentRisk.color;
            currentRiskBadge.style.borderColor = this.currentRisk.color;
        }

        // Atualizar data de última modificação
        const lastUpdated = document.getElementById('lastUpdated');
        if (lastUpdated && this.currentRisk) {
            const date = new Date(this.currentRisk.updated_at);
            lastUpdated.textContent = `Última atualização: ${date.toLocaleString('pt-BR')}`;
        }

        // Atualizar display principal
        const mainRiskDisplay = document.getElementById('mainRiskDisplay');
        const mainRiskDescription = document.getElementById('mainRiskDescription');
        const riskIcon = document.getElementById('riskIcon');

        if (mainRiskDisplay && this.currentRisk) {
            mainRiskDisplay.textContent = this.currentRisk.display;
            mainRiskDisplay.style.color = this.currentRisk.color;
        }

        if (mainRiskDescription && this.currentRisk) {
            const descriptions = {
                'baixo': 'Situação normal, monitoramento de rotina',
                'medio': 'Atenção necessária, monitoramento aumentado',
                'alto': 'Situação de alerta, ação imediata recomendada',
                'critico': 'Perigo iminente, ação urgente necessária'
            };
            mainRiskDescription.textContent = descriptions[this.currentRisk.value] || 'Nível de risco';
        }

        if (riskIcon && this.currentRisk) {
            riskIcon.style.color = this.currentRisk.color;

            // Mudar ícone baseado no nível
            const icons = {
                'baixo': 'fas fa-shield-alt',
                'medio': 'fas fa-exclamation-circle',
                'alto': 'fas fa-exclamation-triangle',
                'critico': 'fas fa-skull'
            };
            riskIcon.className = icons[this.currentRisk.value] || 'fas fa-exclamation-triangle';
        }

        // Atualizar descrição do risco
        const riskDescription = document.getElementById('riskDescription');
        if (riskDescription && this.currentRisk) {
            const descriptions = {
                'baixo': 'Situação controlada. O sistema está operando dentro dos parâmetros normais. Monitoramento de rotina está ativo.',
                'medio': 'Situação que requer atenção. Alguns indicadores mostram variações que necessitam monitoramento mais frequente.',
                'alto': 'Situação de alerta. Indicadores críticos detectados. Ação imediata é recomendada para prevenir escalação.',
                'critico': 'Perigo iminente. Sistema em estado crítico. Ação urgente necessária. Protocolos de emergência devem ser ativados.'
            };
            riskDescription.textContent = descriptions[this.currentRisk.value] || 'Informação não disponível.';
        }

        // Atualizar botões de ação
        this.updateActionButtons();

        // Atualizar ações rápidas
        this.updateQuickActions();

        // Populate modal select
        this.populateModalSelect();
    }

    updateActionButtons() {
        const escalateBtn = document.getElementById('escalateBtn');
        const deescalateBtn = document.getElementById('deescalateBtn');

        if (escalateBtn && this.currentRisk) {
            const canEscalate = this.currentRisk.value !== 'critico';
            escalateBtn.disabled = !canEscalate;
            escalateBtn.style.opacity = canEscalate ? '1' : '0.5';
        }

        if (deescalateBtn && this.currentRisk) {
            const canDeescalate = this.currentRisk.value !== 'baixo';
            deescalateBtn.disabled = !canDeescalate;
            deescalateBtn.style.opacity = canDeescalate ? '1' : '0.5';
        }
    }

    updateQuickActions() {
        const quickActions = document.getElementById('quickActions');
        if (!quickActions || !this.riskLevels.length) return;

        quickActions.innerHTML = '';

        this.riskLevels.forEach(level => {
            if (level.value === this.currentRisk?.value) return; // Skip current level

            const btn = document.createElement('button');
            btn.className = `risk-quick-btn risk-${level.value}`;
            btn.textContent = level.display;
            btn.onclick = () => this.quickChangeRisk(level.value);

            quickActions.appendChild(btn);
        });
    }

    populateModalSelect() {
        const select = document.getElementById('newRiskLevel');
        if (!select || !this.riskLevels.length) return;

        select.innerHTML = '<option value="">Selecione um nível</option>';

        this.riskLevels.forEach(level => {
            const option = document.createElement('option');
            option.value = level.value;
            option.textContent = level.display;
            option.dataset.color = level.color;

            if (level.value === this.currentRisk?.value) {
                option.disabled = true;
                option.textContent += ' (atual)';
            }

            select.appendChild(option);
        });
    }

    setupEventListeners() {
        // Listener para mudança no select de risco
        const riskSelect = document.getElementById('newRiskLevel');
        if (riskSelect) {
            riskSelect.addEventListener('change', (e) => {
                this.updateRiskPreview(e.target.value);
            });
        }

        // Listener para checkbox de confirmação
        const confirmCheckbox = document.getElementById('confirmRiskChange');
        const confirmBtn = document.getElementById('confirmRiskBtn');

        if (confirmCheckbox && confirmBtn) {
            confirmCheckbox.addEventListener('change', (e) => {
                confirmBtn.disabled = !e.target.checked || !riskSelect?.value;
            });
        }

        // Listener para tecla ESC fechar modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });

        // Click fora do modal para fechar
        const modal = document.getElementById('riskModal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        }
    }

    updateRiskPreview(riskValue) {
        const riskPreview = document.getElementById('riskPreview');
        const riskPreviewText = document.getElementById('riskPreviewText');
        const riskPreviewDescription = document.getElementById('riskPreviewDescription');
        const escalationWarning = document.getElementById('escalationWarning');
        const confirmBtn = document.getElementById('confirmRiskBtn');
        const confirmCheckbox = document.getElementById('confirmRiskChange');

        if (!riskValue) {
            riskPreview.style.display = 'none';
            escalationWarning.style.display = 'none';
            confirmBtn.disabled = true;
            return;
        }

        const selectedRisk = this.riskLevels.find(level => level.value === riskValue);
        if (!selectedRisk) return;

        // Atualizar preview
        riskPreviewText.textContent = selectedRisk.display;
        riskPreviewText.style.color = selectedRisk.color;

        const descriptions = {
            'baixo': 'Situação normal, monitoramento de rotina',
            'medio': 'Atenção necessária, monitoramento aumentado',
            'alto': 'Situação de alerta, ação imediata recomendada',
            'critico': 'Perigo iminente, ação urgente necessária'
        };
        riskPreviewDescription.textContent = descriptions[riskValue] || '';

        riskPreview.style.display = 'block';

        // Mostrar aviso se for escalação
        const currentLevel = this.getCurrentRiskLevel();
        const newLevel = this.getRiskLevel(riskValue);

        if (newLevel > currentLevel) {
            escalationWarning.style.display = 'flex';
        } else {
            escalationWarning.style.display = 'none';
        }

        // Habilitar botão apenas se checkbox estiver marcado
        confirmBtn.disabled = !confirmCheckbox?.checked;
    }

    getCurrentRiskLevel() {
        const levels = { 'baixo': 1, 'medio': 2, 'alto': 3, 'critico': 4 };
        return levels[this.currentRisk?.value] || 1;
    }

    getRiskLevel(riskValue) {
        const levels = { 'baixo': 1, 'medio': 2, 'alto': 3, 'critico': 4 };
        return levels[riskValue] || 1;
    }

    async updateRisk() {
        const newRiskValue = document.getElementById('newRiskLevel').value;

        if (!newRiskValue) {
            this.showNotification('Selecione um nível de risco', 'error');
            return;
        }

        try {
            // Mostrar loading
            const confirmBtn = document.getElementById('confirmRiskBtn');
            const originalText = confirmBtn.innerHTML;
            confirmBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Alterando...';
            confirmBtn.disabled = true;

            const response = await fetch(`${this.API_BASE_URL}/${this.dashboardId}/update-risk/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    risco: newRiskValue
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erro ao alterar risco');
            }

            const data = await response.json();

            // Atualizar dados locais
            this.currentRisk = {
                value: data.new_risk,
                display: data.new_risk_display,
                color: data.new_risk_color,
                updated_at: data.updated_at
            };

            // Atualizar interface
            this.updateInterface();
            this.closeModal();

            this.showNotification(data.message, 'success');
            console.log('Risco atualizado:', data);

        } catch (error) {
            console.error('Erro ao alterar risco:', error);
            this.showNotification(error.message, 'error');
        } finally {
            // Restaurar botão
            const confirmBtn = document.getElementById('confirmRiskBtn');
            if (confirmBtn) {
                confirmBtn.innerHTML = '<i class="fas fa-save"></i> Alterar Risco';
                confirmBtn.disabled = false;
            }
        }
    }

    async quickChangeRisk(newRiskValue) {
        if (confirm(`Tem certeza que deseja alterar o nível de risco para "${this.riskLevels.find(l => l.value === newRiskValue)?.display}"?`)) {
            try {
                const response = await fetch(`${this.API_BASE_URL}/${this.dashboardId}/update-risk/`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        risco: newRiskValue
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Erro ao alterar risco');
                }

                const data = await response.json();

                // Atualizar dados locais
                this.currentRisk = {
                    value: data.new_risk,
                    display: data.new_risk_display,
                    color: data.new_risk_color,
                    updated_at: data.updated_at
                };

                // Atualizar interface
                this.updateInterface();

                this.showNotification(data.message, 'success');

            } catch (error) {
                console.error('Erro ao alterar risco:', error);
                this.showNotification(error.message, 'error');
            }
        }
    }

    async escalateRisk() {
        const riskProgression = ['baixo', 'medio', 'alto', 'critico'];
        const currentIndex = riskProgression.indexOf(this.currentRisk?.value);

        if (currentIndex === -1 || currentIndex >= riskProgression.length - 1) {
            this.showNotification('Não é possível escalar mais o nível de risco', 'info');
            return;
        }

        const nextRisk = riskProgression[currentIndex + 1];
        await this.quickChangeRisk(nextRisk);
    }

    async deescalateRisk() {
        const riskProgression = ['baixo', 'medio', 'alto', 'critico'];
        const currentIndex = riskProgression.indexOf(this.currentRisk?.value);

        if (currentIndex <= 0) {
            this.showNotification('Não é possível reduzir mais o nível de risco', 'info');
            return;
        }

        const previousRisk = riskProgression[currentIndex - 1];
        await this.quickChangeRisk(previousRisk);
    }

    async showRiskHistory() {
        try {
            const response = await fetch(`${this.API_BASE_URL}/${this.dashboardId}/risk-history/`);
            if (!response.ok) throw new Error('Erro ao carregar histórico');

            const data = await response.json();

            this.showNotification('Histórico de risco será implementado em versão futura', 'info');
            console.log('Histórico de risco:', data);

        } catch (error) {
            console.error('Erro ao carregar histórico:', error);
            this.showNotification('Erro ao carregar histórico de risco', 'error');
        }
    }

    openModal() {
        const modal = document.getElementById('riskModal');
        if (modal) {
            modal.style.display = 'flex';

            // Reset form
            document.getElementById('newRiskLevel').value = '';
            document.getElementById('confirmRiskChange').checked = false;
            document.getElementById('riskPreview').style.display = 'none';
            document.getElementById('escalationWarning').style.display = 'none';
            document.getElementById('confirmRiskBtn').disabled = true;

            // Atualizar display do risco atual
            const currentRiskDisplay = document.getElementById('currentRiskDisplay');
            if (currentRiskDisplay && this.currentRisk) {
                currentRiskDisplay.textContent = this.currentRisk.display;
                currentRiskDisplay.style.color = this.currentRisk.color;
            }
        }
    }

    closeModal() {
        const modal = document.getElementById('riskModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    showNotification(message, type = 'info') {
        // Remover notificações existentes
        const existingNotifications = document.querySelectorAll('.risk-notification');
        existingNotifications.forEach(n => n.remove());

        // Criar notificação
        const notification = document.createElement('div');
        notification.className = `risk-notification risk-notification-${type}`;

        const icon = type === 'success' ? 'check-circle' :
            type === 'error' ? 'exclamation-circle' : 'info-circle';

        notification.innerHTML = `
                    <i class="fas fa-${icon}"></i>
                    <span>${message}</span>
                    <button onclick="this.parentElement.remove()">&times;</button>
                `;

        document.body.appendChild(notification);

        // Remover após 5 segundos
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    setupDateTime() {
        const updateDateTime = () => {
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
        };

        updateDateTime();
        setInterval(updateDateTime, 1000);
    }

    // Método para recarregar dados
    async refresh() {
        await this.loadCurrentRisk();
        this.updateInterface();
        this.showNotification('Dados atualizados', 'success');
    }
}

// Inicializar o gerenciador de risco
let riskManager;

document.addEventListener('DOMContentLoaded', () => {
    console.log('Inicializando Chirp Risk Management...');
    riskManager = new RiskManager(window.DASHBOARD_ID);

    // Atualizar dados a cada 30 segundos
    setInterval(() => {
        if (riskManager) {
            riskManager.loadCurrentRisk().then(() => {
                riskManager.updateInterface();
            });
        }
    }, 30000);
});

// Funções globais para debug
function debugRiskManager() {
    console.log('=== CHIRP RISK MANAGEMENT DEBUG ===');
    console.log('Dashboard ID:', window.DASHBOARD_ID);
    console.log('Current Risk:', riskManager?.currentRisk);
    console.log('Risk Levels:', riskManager?.riskLevels);
    console.log('====================================');
}

function forceRefresh() {
    if (riskManager) {
        riskManager.refresh();
    }
}