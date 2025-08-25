from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import random

dashboard_api = Blueprint('dashboard_api', __name__, url_prefix='/api')

# ===== DADOS FICTÍCIOS =====

# Categorias fictícias
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

# Transações fictícias
def gerar_transacoes_ficticias():
    transacoes = []
    hoje = datetime.now()
    
    # Gerar transações dos últimos 30 dias com tipos corretos
    transacoes_fixas = [
        # Receitas
        {'descricao': 'Salário', 'tipo': 'receita', 'categoria_nome': 'Salário', 'valor': 4500.00},
        {'descricao': 'Freelance Web Design', 'tipo': 'receita', 'categoria_nome': 'Freelance', 'valor': 800.00},
        {'descricao': 'Dividendos', 'tipo': 'receita', 'categoria_nome': 'Investimentos', 'valor': 120.00},
        {'descricao': 'Venda Notebook', 'tipo': 'receita', 'categoria_nome': 'Outros', 'valor': 1200.00},
        
        # Despesas
        {'descricao': 'Supermercado', 'tipo': 'despesa', 'categoria_nome': 'Alimentação', 'valor': 85.50},
        {'descricao': 'Restaurante', 'tipo': 'despesa', 'categoria_nome': 'Alimentação', 'valor': 45.00},
        {'descricao': 'Padaria', 'tipo': 'despesa', 'categoria_nome': 'Alimentação', 'valor': 15.00},
        {'descricao': 'Uber', 'tipo': 'despesa', 'categoria_nome': 'Transporte', 'valor': 25.00},
        {'descricao': 'Gasolina', 'tipo': 'despesa', 'categoria_nome': 'Transporte', 'valor': 120.00},
        {'descricao': 'Aluguel', 'tipo': 'despesa', 'categoria_nome': 'Moradia', 'valor': 800.00},
        {'descricao': 'Conta de Luz', 'tipo': 'despesa', 'categoria_nome': 'Moradia', 'valor': 95.00},
        {'descricao': 'Internet', 'tipo': 'despesa', 'categoria_nome': 'Moradia', 'valor': 80.00},
        {'descricao': 'Cinema', 'tipo': 'despesa', 'categoria_nome': 'Lazer', 'valor': 30.00},
    ]
    
    # Gerar transações com base nas fixas
    for i, base in enumerate(transacoes_fixas * 3):  # Repetir para ter mais dados
        # Variar as datas
        dias_atras = random.randint(0, 30)
        data = hoje - timedelta(days=dias_atras)
        
        # Variar valores ligeiramente
        valor_variacao = random.uniform(0.8, 1.2)
        valor_final = base['valor'] * valor_variacao
        
        # Encontrar categoria_id baseado no nome
        categoria_id = 1
        for cat in CATEGORIAS_FICTICIAS:
            if cat['nome'] == base['categoria_nome']:
                categoria_id = cat['id']
                break
        
        transacao = {
            'id': i + 1,
            'descricao': base['descricao'],
            'valor': round(valor_final, 2),
            'tipo': base['tipo'],
            'data_transacao': data.isoformat(),
            'categoria_id': categoria_id,
            'categoria_nome': base['categoria_nome'],
            'observacoes': random.choice(['', '', '', 'Observação importante', 'Lembrar de verificar'])
        }
        transacoes.append(transacao)
        
        if len(transacoes) >= 50:  # Limitar a 50 transações
            break
    
    return sorted(transacoes, key=lambda x: x['data_transacao'], reverse=True)

TRANSACOES_FICTICIAS = gerar_transacoes_ficticias()

def calcular_resumo_mes():
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1)
    
    receitas_mes = 0
    despesas_mes = 0
    
    for transacao in TRANSACOES_FICTICIAS:
        data_transacao = datetime.fromisoformat(transacao['data_transacao'])
        if data_transacao >= inicio_mes:
            if transacao['tipo'] == 'receita':
                receitas_mes += transacao['valor']
            else:
                despesas_mes += transacao['valor']
    
    saldo_atual = receitas_mes - despesas_mes + random.uniform(1000, 5000)  # Saldo anterior fictício
    
    # Preparar dados para gráficos
    fluxo_caixa = {
        'labels': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
        'receitas': [3500, 4200, 3800, 4500, 4000, receitas_mes],
        'despesas': [2800, 3200, 2900, 3100, 2700, despesas_mes]
    }
    
    # Gastos por categoria (últimos 6 valores do mês atual)
    gastos_por_categoria = [
        {'nome': 'Alimentação', 'total': 600},
        {'nome': 'Transporte', 'total': 400},
        {'nome': 'Moradia', 'total': 800},
        {'nome': 'Lazer', 'total': 300},
        {'nome': 'Saúde', 'total': 200},
        {'nome': 'Outros', 'total': 500}
    ]
    
    return {
        'receitas_mes': round(receitas_mes, 2),
        'despesas_mes': round(despesas_mes, 2),
        'saldo_atual': round(saldo_atual, 2),
        'transacoes_recentes': TRANSACOES_FICTICIAS[:10],
        'fluxo_caixa': fluxo_caixa,
        'gastos_por_categoria': gastos_por_categoria
    }

def gerar_estatisticas_ficticias():
    # Dados para gráficos
    hoje = datetime.now()
    
    # Últimos 7 dias
    gastos_semanais = []
    for i in range(7):
        data = hoje - timedelta(days=i)
        valor = random.uniform(0, 200)
        gastos_semanais.append({
            'data': data.strftime('%Y-%m-%d'),
            'valor': round(valor, 2)
        })
    
    # Por categoria - com estrutura correta
    categorias_nomes = ['Alimentação', 'Transporte', 'Moradia', 'Lazer', 'Saúde', 'Outros']
    cores_categorias = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#FFD93D']
    
    gastos_categoria = []
    for i, categoria in enumerate(categorias_nomes):
        valor = random.uniform(100, 1000)
        gastos_categoria.append({
            'categoria': categoria,
            'valor': round(valor, 2),
            'cor': cores_categorias[i]
        })
    
    # Comparativo mensal
    meses = []
    for i in range(6):
        data = hoje - timedelta(days=30*i)
        receitas = random.uniform(3000, 6000)
        despesas = random.uniform(2000, 4500)
        meses.append({
            'mes': data.strftime('%b'),
            'receitas': round(receitas, 2),
            'despesas': round(despesas, 2)
        })
    
    # Dados para gráficos do dashboard
    dados_dashboard = {
        'labels': [d['data'] for d in reversed(gastos_semanais)],
        'datasets': [
            {
                'label': 'Gastos Diários',
                'data': [d['valor'] for d in reversed(gastos_semanais)],
                'backgroundColor': '#FF6B6B',
                'borderColor': '#FF6B6B',
                'tension': 0.4
            }
        ]
    }
    
    return {
        'gastos_semanais': list(reversed(gastos_semanais)),
        'gastos_categoria': gastos_categoria,
        'comparativo_mensal': list(reversed(meses)),
        'dados_dashboard': dados_dashboard
    }

# ===== ROTAS DA API =====

@dashboard_api.route('/dashboard/resumo')
@login_required
def dashboard_resumo():
    """Retorna resumo do dashboard com dados fictícios"""
    try:
        resumo = calcular_resumo_mes()
        return jsonify(resumo)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_api.route('/dashboard/estatisticas')
@login_required
def dashboard_estatisticas():
    """Retorna estatísticas para gráficos com dados fictícios"""
    try:
        estatisticas = gerar_estatisticas_ficticias()
        return jsonify(estatisticas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_api.route('/categorias')
@login_required
def get_categorias():
    """Retorna categorias fictícias"""
    try:
        return jsonify(CATEGORIAS_FICTICIAS)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_api.route('/categorias/<int:categoria_id>')
@login_required
def get_categoria(categoria_id):
    """Retorna uma categoria específica"""
    try:
        categoria = next((c for c in CATEGORIAS_FICTICIAS if c['id'] == categoria_id), None)
        if not categoria:
            return jsonify({'error': 'Categoria não encontrada'}), 404
        return jsonify(categoria)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_api.route('/despesas')
@login_required  
def get_despesas():
    """Retorna lista de transações fictícias"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Simular paginação
        inicio = (page - 1) * per_page
        fim = inicio + per_page
        
        transacoes_pagina = TRANSACOES_FICTICIAS[inicio:fim]
        
        return jsonify(transacoes_pagina)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_api.route('/despesas/<int:transacao_id>')
@login_required
def get_despesa(transacao_id):
    """Retorna uma transação específica"""
    try:
        transacao = next((t for t in TRANSACOES_FICTICIAS if t['id'] == transacao_id), None)
        if not transacao:
            return jsonify({'error': 'Transação não encontrada'}), 404
        return jsonify(transacao)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_api.route('/despesas', methods=['POST'])
@login_required
def create_despesa():
    """Cria uma nova transação fictícia"""
    try:
        data = request.get_json()
        
        # Simular criação
        nova_transacao = {
            'id': len(TRANSACOES_FICTICIAS) + 1,
            'descricao': data.get('descricao', 'Nova transação'),
            'valor': float(data.get('valor', 0)),
            'tipo': data.get('tipo', 'despesa'),
            'data_transacao': data.get('data_transacao', datetime.now().isoformat()),
            'categoria_id': int(data.get('categoria_id', 1)),
            'categoria_nome': next((c['nome'] for c in CATEGORIAS_FICTICIAS if c['id'] == int(data.get('categoria_id', 1))), 'Outros'),
            'observacoes': data.get('observacoes', '')
        }
        
        TRANSACOES_FICTICIAS.insert(0, nova_transacao)
        
        return jsonify({
            'success': True,
            'message': 'Transação criada com sucesso',
            'data': nova_transacao
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@dashboard_api.route('/despesas/<int:transacao_id>', methods=['PUT'])
@login_required
def update_despesa(transacao_id):
    """Atualiza uma transação fictícia"""
    try:
        data = request.get_json()
        
        # Encontrar e atualizar transação
        for i, transacao in enumerate(TRANSACOES_FICTICIAS):
            if transacao['id'] == transacao_id:
                TRANSACOES_FICTICIAS[i].update({
                    'descricao': data.get('descricao', transacao['descricao']),
                    'valor': float(data.get('valor', transacao['valor'])),
                    'tipo': data.get('tipo', transacao['tipo']),
                    'data_transacao': data.get('data_transacao', transacao['data_transacao']),
                    'categoria_id': int(data.get('categoria_id', transacao['categoria_id'])),
                    'categoria_nome': next((c['nome'] for c in CATEGORIAS_FICTICIAS if c['id'] == int(data.get('categoria_id', transacao['categoria_id']))), transacao['categoria_nome']),
                    'observacoes': data.get('observacoes', transacao['observacoes'])
                })
                
                return jsonify({
                    'success': True,
                    'message': 'Transação atualizada com sucesso',
                    'data': TRANSACOES_FICTICIAS[i]
                })
        
        return jsonify({'success': False, 'message': 'Transação não encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@dashboard_api.route('/despesas/<int:transacao_id>', methods=['DELETE'])
@login_required
def delete_despesa(transacao_id):
    """Exclui uma transação fictícia"""
    try:
        # Encontrar e remover transação
        for i, transacao in enumerate(TRANSACOES_FICTICIAS):
            if transacao['id'] == transacao_id:
                del TRANSACOES_FICTICIAS[i]
                return jsonify({
                    'success': True,
                    'message': 'Transação excluída com sucesso'
                })
        
        return jsonify({'success': False, 'message': 'Transação não encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
