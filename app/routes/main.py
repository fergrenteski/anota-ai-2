from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from datetime import datetime
import random

main_bp = Blueprint('main', __name__)

# ===== DADOS FICTÍCIOS =====

# Categorias fictícias (importadas do dashboard_api)
CATEGORIAS_FICTICIAS = [
    {'id': 1, 'nome': 'Alimentação', 'tipo': 'despesa', 'cor': '#FF6B6B'},
    {'id': 2, 'nome': 'Transporte', 'tipo': 'despesa', 'cor': '#4ECDC4'},
    {'id': 3, 'nome': 'Moradia', 'tipo': 'despesa', 'cor': '#45B7D1'},
    {'id': 4, 'nome': 'Lazer', 'tipo': 'despesa', 'cor': '#96CEB4'},
    {'id': 5, 'nome': 'Saúde', 'tipo': 'despesa', 'cor': '#FFEAA7'},
    {'id': 6, 'nome': 'Educação', 'tipo': 'despesa', 'cor': '#DDA0DD'},
    {'id': 7, 'nome': 'Salário', 'tipo': 'receita', 'cor': '#98D8C8'},
    {'id': 8, 'nome': 'Freelance', 'tipo': 'receita', 'cor': '#A8E6CF'},
    {'id': 9, 'nome': 'Investimentos', 'tipo': 'receita', 'cor': '#B4E7CE'},
    {'id': 10, 'nome': 'Outros', 'tipo': 'ambos', 'cor': '#FFD93D'},
]

# Dicas fictícias
DICAS_FICTICIAS = [
    {
        'id': 1,
        'titulo': 'Como economizar no supermercado',
        'conteudo': 'Faça uma lista antes de ir às compras e estabeleça um orçamento máximo.',
        'categoria': 'economia'
    },
    {
        'id': 2,
        'titulo': 'Investimentos para iniciantes',
        'conteudo': 'Comece com a poupança e depois considere CDBs e fundos de investimento.',
        'categoria': 'investimentos'
    },
    {
        'id': 3,
        'titulo': 'Controle de gastos mensais',
        'conteudo': 'Registre todas as suas despesas diariamente para ter controle total.',
        'categoria': 'planejamento'
    }
]

# ===== ROTAS PRINCIPAIS =====

@main_bp.route('/')
def index():
    """Página inicial - redireciona para dashboard se logado"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Página principal do dashboard"""
    try:
        # Dados fictícios para o dashboard
        dashboard_data = {
            'receitas_mes': 4500.00,
            'despesas_mes': 2800.00,
            'saldo_atual': 8750.00,
            'usuario_nome': current_user.nome
        }
        return render_template('dashboard.html', **dashboard_data)
    except Exception as e:
        return render_template('dashboard.html', error=str(e))

# ===== ROTAS DE AUTENTICAÇÃO =====

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login do usuário"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Login fictício - aceita qualquer email/senha, mas sugere demo
        if email == 'demo@anotaai.com' and password == 'demo123':
            from app import USUARIO_DEMO
            login_user(USUARIO_DEMO, remember=True)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        elif email and password:
            # Aceita qualquer combinação válida para demonstração
            from app import USUARIO_DEMO
            login_user(USUARIO_DEMO, remember=True)
            flash('Login realizado com sucesso! (Modo demonstração)', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Email e senha são obrigatórios.', 'danger')
    
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de novo usuário"""
    if request.method == 'POST':
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main_bp.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('main.login'))

# ===== ROTAS DE PERFIL =====

@main_bp.route('/perfil')
@login_required
def perfil():
    """Página de perfil do usuário"""
    return render_template('perfil.html', usuario=current_user)

@main_bp.route('/perfil/update', methods=['POST'])
@login_required
def update_perfil():
    """Atualiza perfil do usuário"""
    flash('Perfil atualizado com sucesso!', 'success')
    return redirect(url_for('main.perfil'))

@main_bp.route('/perfil/change-password', methods=['POST'])
@login_required
def change_password():
    """Altera senha do usuário"""
    flash('Senha alterada com sucesso!', 'success')
    return redirect(url_for('main.perfil'))

# ===== ROTAS DE CATEGORIAS =====

@main_bp.route('/categorias')
@login_required
def categorias():
    """Página de gerenciamento de categorias"""
    return render_template('categorias.html', categorias=CATEGORIAS_FICTICIAS)

@main_bp.route('/categorias/create', methods=['POST'])
@login_required
def create_categoria():
    """Cria nova categoria"""
    flash('Categoria criada com sucesso!', 'success')
    return redirect(url_for('main.categorias'))

# ===== ROTAS DE DESPESAS =====

@main_bp.route('/despesas-receitas')
@login_required
def despesas_receitas():
    """Página de gerenciamento de despesas e receitas"""
    # Buscar algumas transações da API fictícia
    try:
        from app.routes.dashboard_api import TRANSACOES_FICTICIAS
        transacoes = TRANSACOES_FICTICIAS[:20]
    except ImportError:
        # Fallback com transações fictícias básicas
        transacoes = [
            {
                'id': 1,
                'descricao': 'Supermercado',
                'valor': 85.50,
                'tipo': 'despesa',
                'data_transacao': '2025-08-25',
                'categoria_nome': 'Alimentação'
            },
            {
                'id': 2,
                'descricao': 'Salário',
                'valor': 3500.00,
                'tipo': 'receita',
                'data_transacao': '2025-08-01',
                'categoria_nome': 'Salário'
            }
        ]
    
    return render_template('despesas_receitas.html', 
                         despesas=transacoes,
                         categorias=CATEGORIAS_FICTICIAS)

# ===== ROTAS DE DICAS =====

@main_bp.route('/dicas')
def dicas():
    """Página de dicas financeiras"""
    return render_template('dicas.html', dicas=DICAS_FICTICIAS)

@main_bp.route('/dicas/<int:dica_id>')
def show_dica(dica_id):
    """Mostra detalhes de uma dica"""
    dica = next((d for d in DICAS_FICTICIAS if d['id'] == dica_id), None)
    if not dica:
        flash('Dica não encontrada.', 'danger')
        return redirect(url_for('main.dicas'))
    return render_template('dica_detalhes.html', dica=dica)

# ===== ROTAS DE RELATÓRIOS =====

@main_bp.route('/relatorio-mensal')
@login_required
def relatorio_mensal():
    """Página de relatório mensal"""
    # Dados fictícios para relatório
    dados = {
        'total_receitas': 4500.00,
        'total_despesas': 2800.00,
        'saldo_mes': 1700.00,
        'maior_despesa': 'Aluguel - R$ 800,00',
        'categoria_maior_gasto': 'Moradia'
    }
    
    # Dados fictícios para o gráfico mensal - estrutura correta
    dados_grafico = {
        'labels': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
        'categorias': ['Alimentação', 'Transporte', 'Moradia', 'Lazer', 'Outros'],
        'cores': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFD93D'],
        'dados': {
            'Alimentação': [450, 520, 480, 600, 550, 600],
            'Transporte': [300, 280, 320, 350, 300, 400],
            'Moradia': [800, 800, 800, 800, 800, 800],
            'Lazer': [200, 150, 300, 250, 400, 300],
            'Outros': [150, 200, 180, 220, 200, 700]
        }
    }
    
    return render_template('relatorio_mensal.html', dados=dados, dados_grafico=dados_grafico)

@main_bp.route('/relatorio-semanal')
@login_required
def relatorio_semanal():
    """Página de relatório semanal"""
    # Dados fictícios para o gráfico semanal
    dados_grafico = {
        'labels': ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
        'categorias': ['Alimentação', 'Transporte', 'Moradia', 'Lazer', 'Outros'],
        'cores': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFD93D'],
        'dados': {
            'Alimentação': [120, 150, 130, 140],
            'Transporte': [80, 90, 85, 95],
            'Moradia': [800, 800, 800, 800],
            'Lazer': [200, 150, 180, 170],
            'Outros': [100, 80, 120, 90]
        }
    }
    
    return render_template('relatorio_semanal.html', dados_grafico=dados_grafico)

@main_bp.route('/relatorio-diario')
@login_required
def relatorio_diario():
    """Página de relatório diário"""
    data = request.args.get('data', datetime.now().strftime('%Y-%m-%d'))
    
    # Dados fictícios para o gráfico diário
    dados_grafico = {
        'labels': ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
        'categorias': ['Alimentação', 'Transporte', 'Moradia', 'Lazer', 'Outros'],
        'cores': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFD93D'],
        'dados': {
            'Alimentação': [25, 30, 20, 35, 40, 50, 30],
            'Transporte': [15, 20, 10, 25, 30, 0, 0],
            'Moradia': [0, 0, 800, 0, 0, 0, 0],
            'Lazer': [0, 0, 0, 0, 80, 120, 60],
            'Outros': [10, 5, 15, 20, 25, 30, 10]
        }
    }
    
    return render_template('relatorio_diario.html', data=data, dados_grafico=dados_grafico)

@main_bp.route('/configuracoes')
@login_required
def configuracoes():
    """Página de configurações"""
    return render_template('configuracoes.html')

# ===== API ROUTES FICTÍCIAS =====

@main_bp.route('/api/categorias')
@login_required
def api_categorias():
    """API para obter categorias do usuário"""
    return jsonify(CATEGORIAS_FICTICIAS)

@main_bp.route('/api/dicas/random')
def api_dicas_random():
    """API para obter dicas aleatórias"""
    dica = random.choice(DICAS_FICTICIAS)
    return jsonify(dica)

@main_bp.route('/api/dashboard')
@login_required
def api_dashboard():
    """API para dados do dashboard"""
    try:
        # Tentar importar dados das transações fictícias
        try:
            from app.routes.dashboard_api import TRANSACOES_FICTICIAS
            transacoes_recentes = TRANSACOES_FICTICIAS[:10]
        except ImportError:
            transacoes_recentes = []
        
        data = {
            'receitas_mes': 4500.00,
            'despesas_mes': 2800.00,
            'saldo_atual': 8750.00,
            'transacoes_recentes': transacoes_recentes
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/search')
def api_search():
    """API endpoint para pesquisa global"""
    query = request.args.get('q', '').strip()
    
    if len(query) < 2:
        return jsonify({'error': 'Termo muito curto'}), 400
    
    # Busca fictícia
    results = [
        {
            'type': 'dica',
            'title': 'Como economizar',
            'description': 'Dicas para economizar no dia a dia',
            'url': '/dicas/1'
        }
    ]
    
    return jsonify({
        'query': query,
        'results': results
    })
