// ===== DASHBOARD SPECIFIC FUNCTIONALITY =====

class DashboardManager {
    constructor() {
        this.api = window.api;
        this.charts = {};
        this.refreshInterval = null;
        
        this.init();
    }

    init() {
        this.loadDashboardData();
        this.setupCharts();
        this.setupEventListeners();
        this.startAutoRefresh();
    }

    // ===== DATA LOADING =====
    async loadDashboardData() {
        try {
            this.showLoadingState();
            
            // Carregar dados do dashboard
            const dashboardData = await this.api.get('/dashboard/resumo');
            
            this.updateSummaryCards(dashboardData);
            this.updateTransactionsList(dashboardData.transacoes_recentes);
            this.updateCharts(dashboardData);
            
        } catch (error) {
            console.error('Erro ao carregar dados do dashboard:', error);
            window.anotaAiApp.showAlert('Erro ao carregar dados do dashboard', 'danger');
        } finally {
            this.hideLoadingState();
        }
    }

    // ===== SUMMARY CARDS =====
    updateSummaryCards(data) {
        // Receitas do mês
        const receitasCard = document.querySelector('[data-card="receitas"]');
        if (receitasCard) {
            const valor = receitasCard.querySelector('.fs-5');
            if (valor) valor.textContent = formatCurrency(data.receitas_mes || 0);
        }

        // Despesas do mês
        const despesasCard = document.querySelector('[data-card="despesas"]');
        if (despesasCard) {
            const valor = despesasCard.querySelector('.fs-5');
            if (valor) valor.textContent = formatCurrency(data.despesas_mes || 0);
        }

        // Saldo atual
        const saldoCard = document.querySelector('[data-card="saldo"]');
        if (saldoCard) {
            const valor = saldoCard.querySelector('.fs-5');
            if (valor) {
                valor.textContent = formatCurrency(data.saldo_atual || 0);
                // Atualizar cor baseado no saldo
                valor.className = `fs-5 fw-bold ${data.saldo_atual >= 0 ? 'text-success' : 'text-danger'}`;
            }
        }

        // Economia
        const economiaCard = document.querySelector('[data-card="economia"]');
        if (economiaCard) {
            const valor = economiaCard.querySelector('.fs-5');
            if (valor) {
                const economia = (data.receitas_mes || 0) - (data.despesas_mes || 0);
                valor.textContent = formatCurrency(economia);
                valor.className = `fs-5 fw-bold ${economia >= 0 ? 'text-success' : 'text-danger'}`;
            }
        }
    }

    // ===== TRANSACTIONS LIST =====
    updateTransactionsList(transacoes) {
        const tbody = document.querySelector('#transacoes-recentes tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (!transacoes || transacoes.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted">
                        Nenhuma transação encontrada
                    </td>
                </tr>
            `;
            return;
        }

        transacoes.forEach(transacao => {
            const row = this.createTransactionRow(transacao);
            tbody.appendChild(row);
        });
    }

    createTransactionRow(transacao) {
        const row = document.createElement('tr');
        
        const isReceita = transacao.tipo === 'receita';
        const iconClass = isReceita ? 'bi-arrow-up-circle text-success' : 'bi-arrow-down-circle text-danger';
        const valorClass = isReceita ? 'text-success' : 'text-danger';
        const sinal = isReceita ? '+' : '-';

        row.innerHTML = `
            <td>
                <div class="d-flex align-items-center">
                    <i class="bi ${iconClass} me-2"></i>
                    <div>
                        <div class="fw-medium">${transacao.descricao}</div>
                        <small class="text-muted">${transacao.categoria_nome}</small>
                    </div>
                </div>
            </td>
            <td class="fw-medium ${valorClass}">
                ${sinal} ${formatCurrency(Math.abs(transacao.valor))}
            </td>
            <td>
                <small class="text-muted">${formatDate(transacao.data_transacao)}</small>
            </td>
            <td>
                <span class="badge ${isReceita ? 'bg-success' : 'bg-danger'}">
                    ${transacao.tipo}
                </span>
            </td>
            <td>
                <div class="dropdown">
                    <button class="btn btn-sm btn-outline-secondary dropdown-toggle" 
                            data-bs-toggle="dropdown">
                        <i class="bi bi-three-dots"></i>
                    </button>
                    <ul class="dropdown-menu">
                        <li>
                            <a class="dropdown-item" href="#" 
                               onclick="editTransaction(${transacao.id})">
                                <i class="bi bi-pencil me-2"></i>Editar
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item text-danger" href="#" 
                               onclick="deleteTransaction(${transacao.id})">
                                <i class="bi bi-trash me-2"></i>Excluir
                            </a>
                        </li>
                    </ul>
                </div>
            </td>
        `;

        return row;
    }

    // ===== CHARTS =====
    setupCharts() {
        this.setupFluxoCaixaChart();
        this.setupCategoriesChart();
    }

    setupFluxoCaixaChart() {
        const ctx = document.getElementById('fluxoCaixaChart');
        if (!ctx) return;

        this.charts.fluxoCaixa = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Receitas',
                    data: [],
                    borderColor: 'rgb(25, 135, 84)',
                    backgroundColor: 'rgba(25, 135, 84, 0.1)',
                    tension: 0.4
                }, {
                    label: 'Despesas',
                    data: [],
                    borderColor: 'rgb(220, 53, 69)',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                interaction: {
                    intersect: false,
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return formatCurrency(value);
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + formatCurrency(context.parsed.y);
                            }
                        }
                    }
                }
            }
        });
    }

    setupCategoriesChart() {
        const ctx = document.getElementById('categoriesChart');
        if (!ctx) return;

        this.charts.categories = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40',
                        '#FF6384',
                        '#C9CBCF'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = formatCurrency(context.parsed);
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    updateCharts(data) {
        this.updateFluxoCaixaChart(data.fluxo_caixa);
        this.updateCategoriesChart(data.gastos_por_categoria);
    }

    updateFluxoCaixaChart(fluxoData) {
        if (!this.charts.fluxoCaixa || !fluxoData) return;

        const chart = this.charts.fluxoCaixa;
        chart.data.labels = fluxoData.labels;
        chart.data.datasets[0].data = fluxoData.receitas;
        chart.data.datasets[1].data = fluxoData.despesas;
        chart.update();
    }

    updateCategoriesChart(categoriesData) {
        if (!this.charts.categories || !categoriesData) return;

        const chart = this.charts.categories;
        chart.data.labels = categoriesData.map(item => item.nome);
        chart.data.datasets[0].data = categoriesData.map(item => item.total);
        chart.update();
    }

    // ===== EVENT LISTENERS =====
    setupEventListeners() {
        // Botão nova transação
        const btnNovaTransacao = document.querySelector('[data-action="nova-transacao"]');
        if (btnNovaTransacao) {
            btnNovaTransacao.addEventListener('click', () => {
                this.showTransactionModal();
            });
        }

        // Botão atualizar dados
        const btnRefresh = document.querySelector('[data-action="refresh"]');
        if (btnRefresh) {
            btnRefresh.addEventListener('click', () => {
                this.loadDashboardData();
            });
        }

        // Filtro de período
        const periodoSelect = document.querySelector('[data-filter="periodo"]');
        if (periodoSelect) {
            periodoSelect.addEventListener('change', (e) => {
                this.filterByPeriod(e.target.value);
            });
        }
    }

    // ===== MODAL NOVA TRANSAÇÃO =====
    showTransactionModal() {
        // Implementar modal de nova transação
        const modal = new bootstrap.Modal(document.getElementById('modalNovaTransacao'));
        modal.show();
    }

    // ===== FILTROS =====
    async filterByPeriod(periodo) {
        try {
            const data = await this.api.get(`/dashboard/resumo?periodo=${periodo}`);
            this.updateSummaryCards(data);
            this.updateCharts(data);
        } catch (error) {
            console.error('Erro ao filtrar por período:', error);
            window.anotaAiApp.showAlert('Erro ao filtrar dados', 'danger');
        }
    }

    // ===== AUTO REFRESH =====
    startAutoRefresh() {
        // Atualizar dados a cada 5 minutos
        this.refreshInterval = setInterval(() => {
            this.loadDashboardData();
        }, 300000);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    // ===== LOADING STATES =====
    showLoadingState() {
        const loadingElements = document.querySelectorAll('[data-loading]');
        loadingElements.forEach(el => {
            el.classList.add('loading');
        });
    }

    hideLoadingState() {
        const loadingElements = document.querySelectorAll('[data-loading]');
        loadingElements.forEach(el => {
            el.classList.remove('loading');
        });
    }
}

// ===== GLOBAL FUNCTIONS FOR DASHBOARD =====

async function editTransaction(id) {
    try {
        const transaction = await window.api.get(`/despesas/${id}`);
        // Preencher modal de edição com dados da transação
        showEditTransactionModal(transaction);
    } catch (error) {
        console.error('Erro ao carregar transação:', error);
        window.anotaAiApp.showAlert('Erro ao carregar transação', 'danger');
    }
}

async function deleteTransaction(id) {
    if (!confirm('Tem certeza que deseja excluir esta transação?')) {
        return;
    }

    try {
        await window.api.delete(`/despesas/${id}`);
        window.anotaAiApp.showAlert('Transação excluída com sucesso!', 'success');
        
        // Recarregar dados do dashboard
        if (window.dashboardManager) {
            window.dashboardManager.loadDashboardData();
        }
    } catch (error) {
        console.error('Erro ao excluir transação:', error);
        window.anotaAiApp.showAlert('Erro ao excluir transação', 'danger');
    }
}

function showEditTransactionModal(transaction) {
    // Implementar modal de edição
    console.log('Editar transação:', transaction);
}

// ===== INITIALIZE DASHBOARD =====
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se estamos na página do dashboard
    if (window.location.pathname.includes('dashboard') || window.location.pathname === '/') {
        window.dashboardManager = new DashboardManager();
        console.log('Dashboard Manager initialized');
    }
});
