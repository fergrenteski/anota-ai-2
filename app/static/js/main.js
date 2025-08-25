// ===== MAIN JAVASCRIPT - ANOTA-AI =====

class AnotaAiApp {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.mainContent = document.getElementById('main-content');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.saldoAtual = document.getElementById('saldo-atual');
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupActiveNavigation();
        this.setupTooltips();
        this.updateSaldo();
        this.setupResponsiveHandling();
    }

    // ===== EVENT LISTENERS =====
    setupEventListeners() {
        // Mobile Sidebar Toggle
        if (this.sidebarToggle) {
            this.sidebarToggle.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.toggleMobileSidebar();
            });
        }

        // Close sidebar on outside click (mobile only)
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                if (!this.sidebar.contains(e.target) && !this.sidebarToggle.contains(e.target)) {
                    this.closeSidebar();
                }
            }
        });

        // Handle window resize
        window.addEventListener('resize', () => {
            this.handleResize();
        });

        // Search functionality
        const searchForm = document.querySelector('.navbar form');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleSearch();
            });
        }

        // Auto-hide alerts
        this.setupAutoHideAlerts();
    }

    // ===== SIDEBAR FUNCTIONALITY =====
    toggleMobileSidebar() {
        // Funciona apenas em dispositivos móveis
        if (window.innerWidth <= 768) {
            this.sidebar.classList.toggle('show');
        }
    }

    closeSidebar() {
        this.sidebar.classList.remove('show');
    }

    // ===== ACTIVE NAVIGATION =====
    setupActiveNavigation() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            
            // Check if current path matches link href
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
                
                // If it's a submenu item, expand the parent menu
                const parentCollapse = link.closest('.collapse');
                if (parentCollapse) {
                    parentCollapse.classList.add('show');
                }
            }
        });
    }

    // ===== TOOLTIPS =====
    setupTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // ===== SALDO FUNCTIONALITY =====
    updateSaldo(novoSaldo = null) {
        if (novoSaldo !== null && this.saldoAtual) {
            this.saldoAtual.textContent = this.formatCurrency(novoSaldo);
            this.animateSaldoUpdate();
        }
    }

    formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value);
    }

    animateSaldoUpdate() {
        if (this.saldoAtual) {
            this.saldoAtual.parentElement.classList.add('animate__animated', 'animate__pulse');
            setTimeout(() => {
                this.saldoAtual.parentElement.classList.remove('animate__animated', 'animate__pulse');
            }, 1000);
        }
    }

    // ===== SEARCH FUNCTIONALITY =====
    handleSearch() {
        const searchInput = document.querySelector('.navbar .form-control');
        const searchTerm = searchInput ? searchInput.value.trim() : '';
        
        if (searchTerm.length < 2) {
            this.showAlert('Por favor, digite pelo menos 2 caracteres para pesquisar.', 'warning');
            return;
        }

        // Simulate search (replace with actual search implementation)
        this.showAlert(`Pesquisando por: "${searchTerm}"...`, 'info');
        
        // Here you would implement the actual search functionality
        // For example, making an AJAX request to search endpoint
        this.performSearch(searchTerm);
    }

    performSearch(term) {
        // Placeholder for actual search implementation
        fetch(`/api/search?q=${encodeURIComponent(term)}`)
            .then(response => response.json())
            .then(data => {
                // Handle search results
                console.log('Search results:', data);
            })
            .catch(error => {
                console.error('Search error:', error);
                this.showAlert('Erro ao realizar pesquisa. Tente novamente.', 'danger');
            });
    }

    // ===== RESPONSIVE HANDLING =====
    setupResponsiveHandling() {
        // No special setup needed for collapsed state
    }

    handleResize() {
        if (window.innerWidth > 768) {
            // Desktop: remove mobile classes
            this.sidebar.classList.remove('show');
        }
    }

    // ===== ALERT SYSTEM =====
    showAlert(message, type = 'info', duration = 5000) {
        const alertContainer = document.querySelector('.container-fluid');
        if (!alertContainer) return;

        const alertId = 'alert-' + Date.now();
        const alertHTML = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;

        alertContainer.insertAdjacentHTML('afterbegin', alertHTML);

        // Auto-hide alert
        setTimeout(() => {
            const alert = document.getElementById(alertId);
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, duration);
    }

    setupAutoHideAlerts() {
        // Auto-hide existing alerts after 5 seconds
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            setTimeout(() => {
                if (alert && alert.parentNode) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            }, 5000);
        });
    }

    // ===== UTILITY METHODS =====
    
    // Loading state management
    showLoading(element) {
        if (element) {
            element.classList.add('loading');
            element.disabled = true;
        }
    }

    hideLoading(element) {
        if (element) {
            element.classList.remove('loading');
            element.disabled = false;
        }
    }

    // Date formatting
    formatDate(date, options = {}) {
        const defaultOptions = {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };
        
        return new Intl.DateTimeFormat('pt-BR', { ...defaultOptions, ...options }).format(new Date(date));
    }

    // Local storage helpers
    saveToStorage(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    }

    getFromStorage(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Error reading from localStorage:', error);
            return defaultValue;
        }
    }
}

// ===== ADDITIONAL UTILITIES =====

// API Helper Class
class ApiHelper {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// ===== INITIALIZE APPLICATION =====
document.addEventListener('DOMContentLoaded', function() {
    // Initialize main application
    window.anotaAiApp = new AnotaAiApp();
    
    // Initialize API helper
    window.api = new ApiHelper();
    
    // Add fade-in animation to main content
    const mainContent = document.querySelector('.container-fluid');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
    
    console.log('Anota-ai App initialized successfully!');
});

// ===== GLOBAL HELPER FUNCTIONS =====

// Currency formatting
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Date formatting
function formatDate(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    };
    
    return new Intl.DateTimeFormat('pt-BR', { ...defaultOptions, ...options }).format(new Date(date));
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AnotaAiApp, ApiHelper };
}
