// ===== TRANSACTION MANAGEMENT =====

class TransactionManager {
    constructor() {
        this.api = window.api;
        this.categorias = [];
        
        this.init();
    }

    init() {
        this.loadCategorias();
        this.setupEventListeners();
        this.setupFormValidation();
    }

    // ===== CATEGORIAS =====
    async loadCategorias() {
        try {
            this.categorias = await this.api.get('/categorias');
            this.populateCategoriaSelects();
        } catch (error) {
            console.error('Erro ao carregar categorias:', error);
            window.anotaAiApp.showAlert('Erro ao carregar categorias', 'danger');
        }
    }

    populateCategoriaSelects() {
        const selects = [
            document.getElementById('categoriaTransacao'),
            document.getElementById('editCategoriaTransacao')
        ];

        selects.forEach(select => {
            if (!select) return;
            
            select.innerHTML = '<option value="">Selecione uma categoria</option>';
            
            this.categorias.forEach(categoria => {
                const option = document.createElement('option');
                option.value = categoria.id;
                option.textContent = categoria.nome;
                select.appendChild(option);
            });
        });
    }

    // ===== EVENT LISTENERS =====
    setupEventListeners() {
        // Form nova transação
        const formNova = document.getElementById('formNovaTransacao');
        if (formNova) {
            formNova.addEventListener('submit', (e) => {
                e.preventDefault();
                this.createTransaction();
            });
        }

        // Form editar transação
        const formEdit = document.getElementById('formEditarTransacao');
        if (formEdit) {
            formEdit.addEventListener('submit', (e) => {
                e.preventDefault();
                this.updateTransaction();
            });
        }

        // Toggle recorrente
        const recorrenteSelect = document.getElementById('recorrente');
        if (recorrenteSelect) {
            recorrenteSelect.addEventListener('change', (e) => {
                this.toggleFrequenciaField(e.target.value === '1');
            });
        }

        // Tipo de transação change
        const tipoSelect = document.getElementById('tipoTransacao');
        if (tipoSelect) {
            tipoSelect.addEventListener('change', (e) => {
                this.filterCategoriesByType(e.target.value);
            });
        }

        // Data padrão para hoje
        this.setDefaultDate();
    }

    // ===== FORM VALIDATION =====
    setupFormValidation() {
        // Máscara para valor monetário
        const valorInputs = document.querySelectorAll('#valorTransacao, #editValorTransacao');
        valorInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                this.formatCurrencyInput(e.target);
            });
        });
    }

    formatCurrencyInput(input) {
        let value = input.value.replace(/\D/g, '');
        value = (value / 100).toFixed(2);
        input.value = value;
    }

    setDefaultDate() {
        const today = new Date().toISOString().split('T')[0];
        const dateInputs = document.querySelectorAll('#dataTransacao, #editDataTransacao');
        dateInputs.forEach(input => {
            if (!input.value) {
                input.value = today;
            }
        });
    }

    toggleFrequenciaField(show) {
        const container = document.getElementById('frequenciaContainer');
        if (container) {
            container.style.display = show ? 'block' : 'none';
        }
    }

    filterCategoriesByType(tipo) {
        const select = document.getElementById('categoriaTransacao');
        if (!select || !tipo) return;

        // Filtrar categorias baseado no tipo
        const categoriasFiltradas = this.categorias.filter(cat => {
            // Aqui você pode implementar lógica para filtrar categorias por tipo
            // Por exemplo, algumas categorias podem ser específicas para receitas ou despesas
            return true; // Por enquanto, mostrar todas
        });

        select.innerHTML = '<option value="">Selecione uma categoria</option>';
        categoriasFiltradas.forEach(categoria => {
            const option = document.createElement('option');
            option.value = categoria.id;
            option.textContent = categoria.nome;
            select.appendChild(option);
        });
    }

    // ===== CRUD OPERATIONS =====
    async createTransaction() {
        try {
            const formData = this.getFormData('formNovaTransacao');
            
            if (!this.validateTransactionData(formData)) {
                return;
            }

            const button = document.querySelector('#formNovaTransacao button[type="submit"]');
            window.anotaAiApp.showLoading(button);

            const response = await this.api.post('/despesas', formData);

            window.anotaAiApp.showAlert('Transação criada com sucesso!', 'success');
            
            // Fechar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovaTransacao'));
            modal.hide();
            
            // Limpar formulário
            document.getElementById('formNovaTransacao').reset();
            this.setDefaultDate();
            
            // Recarregar dashboard
            if (window.dashboardManager) {
                window.dashboardManager.loadDashboardData();
            }

        } catch (error) {
            console.error('Erro ao criar transação:', error);
            window.anotaAiApp.showAlert('Erro ao criar transação', 'danger');
        } finally {
            const button = document.querySelector('#formNovaTransacao button[type="submit"]');
            window.anotaAiApp.hideLoading(button);
        }
    }

    async updateTransaction() {
        try {
            const formData = this.getFormData('formEditarTransacao');
            const id = formData.id;
            
            if (!this.validateTransactionData(formData) || !id) {
                return;
            }

            const button = document.querySelector('#formEditarTransacao button[type="submit"]');
            window.anotaAiApp.showLoading(button);

            const response = await this.api.put(`/despesas/${id}`, formData);

            window.anotaAiApp.showAlert('Transação atualizada com sucesso!', 'success');
            
            // Fechar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalEditarTransacao'));
            modal.hide();
            
            // Recarregar dashboard
            if (window.dashboardManager) {
                window.dashboardManager.loadDashboardData();
            }

        } catch (error) {
            console.error('Erro ao atualizar transação:', error);
            window.anotaAiApp.showAlert('Erro ao atualizar transação', 'danger');
        } finally {
            const button = document.querySelector('#formEditarTransacao button[type="submit"]');
            window.anotaAiApp.hideLoading(button);
        }
    }

    // ===== HELPERS =====
    getFormData(formId) {
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            if (key === 'valor') {
                data[key] = parseFloat(value);
            } else if (key === 'categoria_id' || key === 'id') {
                data[key] = parseInt(value);
            } else if (key === 'recorrente') {
                data[key] = value === '1';
            } else {
                data[key] = value;
            }
        }
        
        return data;
    }

    validateTransactionData(data) {
        const errors = [];

        if (!data.tipo) {
            errors.push('Tipo é obrigatório');
        }

        if (!data.valor || data.valor <= 0) {
            errors.push('Valor deve ser maior que zero');
        }

        if (!data.categoria_id) {
            errors.push('Categoria é obrigatória');
        }

        if (!data.data_transacao) {
            errors.push('Data é obrigatória');
        }

        if (!data.descricao || data.descricao.trim().length < 3) {
            errors.push('Descrição deve ter pelo menos 3 caracteres');
        }

        if (errors.length > 0) {
            window.anotaAiApp.showAlert('Erros de validação:<br>' + errors.join('<br>'), 'danger');
            return false;
        }

        return true;
    }

    // ===== PUBLIC METHODS =====
    showEditModal(transaction) {
        // Preencher campos do modal de edição
        document.getElementById('editTransacaoId').value = transaction.id;
        document.getElementById('editTipoTransacao').value = transaction.tipo;
        document.getElementById('editValorTransacao').value = Math.abs(transaction.valor);
        document.getElementById('editCategoriaTransacao').value = transaction.categoria_id;
        document.getElementById('editDataTransacao').value = transaction.data_transacao;
        document.getElementById('editDescricaoTransacao').value = transaction.descricao;
        document.getElementById('editObservacoes').value = transaction.observacoes || '';

        // Mostrar modal
        const modal = new bootstrap.Modal(document.getElementById('modalEditarTransacao'));
        modal.show();
    }

    async deleteTransaction(id) {
        if (!confirm('Tem certeza que deseja excluir esta transação?')) {
            return;
        }

        try {
            await this.api.delete(`/despesas/${id}`);
            window.anotaAiApp.showAlert('Transação excluída com sucesso!', 'success');
            
            // Recarregar dashboard
            if (window.dashboardManager) {
                window.dashboardManager.loadDashboardData();
            }
        } catch (error) {
            console.error('Erro ao excluir transação:', error);
            window.anotaAiApp.showAlert('Erro ao excluir transação', 'danger');
        }
    }
}

// ===== GLOBAL FUNCTIONS =====
function showEditTransactionModal(transaction) {
    if (window.transactionManager) {
        window.transactionManager.showEditModal(transaction);
    }
}

// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', function() {
    window.transactionManager = new TransactionManager();
    console.log('Transaction Manager initialized');
});
