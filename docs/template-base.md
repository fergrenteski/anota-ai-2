# Página Base - Anota-ai

## Descrição

Esta página base foi criada com Bootstrap e cores claras, oferecendo uma interface moderna e responsiva para o sistema de controle financeiro Anota-ai.

## Características

### Design
- **Bootstrap 5.3.0**: Framework CSS responsivo
- **Bootstrap Icons**: Ícones consistentes
- **Cores claras**: Design limpo e profissional
- **Responsivo**: Funciona em desktop, tablet e mobile

### Menu Lateral
- **Dashboard**: Página principal com resumos e gráficos
- **Despesas/Receitas**: Gerenciamento de transações financeiras
- **Categorias**: Organização das categorias de gastos
- **Relatórios**: 
  - Mensal
  - Semanal
  - Diário
- **Dicas**: Dicas financeiras e metas

### Barra Superior
- **Toggle do menu**: Recolher/expandir sidebar
- **Barra de pesquisa**: Pesquisa global no sistema
- **Saldo atual**: Exibição do saldo em tempo real
- **Menu do usuário**: Avatar e opções da conta

## Personalização de Cores

O arquivo `app/static/css/main.css` contém variáveis CSS no topo que facilitam a personalização:

```css
:root {
    /* Cores Primárias */
    --primary-color: #4a90e2;
    --primary-hover: #357abd;
    --secondary-color: #6c757d;
    
    /* Cores de Fundo */
    --bg-light: #f8f9fa;
    --bg-white: #ffffff;
    --bg-sidebar: #ffffff;
    --bg-navbar: #ffffff;
    
    /* Cores de Texto */
    --text-primary: #2c3e50;
    --text-secondary: #6c757d;
    --text-light: #ffffff;
    --text-muted: #8e9aaf;
    
    /* Cores de Estado */
    --success-color: #28a745;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --info-color: #17a2b8;
}
```

### Como Personalizar

1. **Alterar cor primária**: Modifique `--primary-color` e `--primary-hover`
2. **Mudar cores de fundo**: Ajuste as variáveis `--bg-*`
3. **Personalizar cores de texto**: Modifique as variáveis `--text-*`
4. **Ajustar cores de estado**: Altere `--success-color`, `--warning-color`, etc.

## Funcionalidades JavaScript

O arquivo `app/static/js/main.js` inclui:

### Classe Principal `AnotaAiApp`
- **Toggle do sidebar**: Recolher/expandir menu lateral
- **Navegação ativa**: Destaque automático da página atual
- **Pesquisa**: Sistema de busca global
- **Alertas**: Sistema de notificações
- **Responsividade**: Adaptação para mobile
- **Atualização de saldo**: Função para atualizar saldo em tempo real

### Helpers Globais
- **formatCurrency()**: Formatação de moeda brasileira
- **formatDate()**: Formatação de datas
- **debounce()**: Função de debounce para pesquisa
- **ApiHelper**: Classe para requisições AJAX

## Estrutura de Arquivos

```
app/
├── static/
│   ├── css/
│   │   └── main.css          # Estilos personalizados
│   ├── js/
│   │   └── main.js           # JavaScript principal
│   └── images/
│       └── default-avatar.svg # Avatar padrão
├── templates/
│   ├── base.html            # Template base
│   ├── dashboard.html       # Página principal
│   └── [outras páginas]     # Páginas específicas
└── routes/
    └── main.py              # Rotas principais
```

## Como Estender

### Adicionando Nova Página

1. **Crie o template** em `app/templates/`:
```html
{% extends "base.html" %}

{% block title %}Minha Página - Anota-ai{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1 class="h3 mb-4">Minha Página</h1>
    </div>
</div>
<!-- Seu conteúdo aqui -->
{% endblock %}
```

2. **Adicione a rota** em `app/routes/main.py`:
```python
@main_bp.route('/minha-pagina')
def minha_pagina():
    return render_template('minha_pagina.html')
```

3. **Adicione no menu** em `base.html`:
```html
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('main.minha_pagina') }}">
        <i class="bi bi-icon"></i>
        <span>Minha Página</span>
    </a>
</li>
```

### Adicionando CSS Personalizado

Adicione seus estilos no final de `main.css` ou crie um novo arquivo CSS e inclua no template:

```html
{% block extra_css %}
    <link href="{{ url_for('static', filename='css/meu-estilo.css') }}" rel="stylesheet">
{% endblock %}
```

### Adicionando JavaScript Personalizado

Adicione seu JavaScript no final de `main.js` ou crie um novo arquivo:

```html
{% block extra_js %}
    <script src="{{ url_for('static', filename='js/meu-script.js') }}"></script>
{% endblock %}
```

## Componentes Responsivos

### Cards de Resumo
```html
<div class="col-lg-3 col-md-6 mb-3">
    <div class="card h-100">
        <div class="card-body">
            <!-- Conteúdo do card -->
        </div>
    </div>
</div>
```

### Tabelas Responsivas
```html
<div class="table-responsive">
    <table class="table table-hover">
        <!-- Conteúdo da tabela -->
    </table>
</div>
```

### Alertas com Auto-hide
```javascript
window.anotaAiApp.showAlert('Mensagem', 'success', 5000);
```

## Ícones Disponíveis

O projeto usa Bootstrap Icons. Alguns ícones úteis:
- `bi-speedometer2`: Dashboard
- `bi-cash-stack`: Dinheiro/Transações
- `bi-tags-fill`: Categorias
- `bi-graph-up`: Relatórios
- `bi-lightbulb-fill`: Dicas
- `bi-person-circle`: Usuário
- `bi-gear`: Configurações

## APIs Disponíveis

### Busca
- **GET** `/api/search?q=termo`: Pesquisa global

### Saldo
- **GET** `/api/saldo`: Retorna saldo atual

## Suporte a Acessibilidade

O template inclui:
- Navegação por teclado
- Labels ARIA apropriados
- Contraste adequado de cores
- Estrutura semântica HTML5

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Performance

- CSS e JS minificados em produção
- Imagens otimizadas
- Lazy loading para conteúdo dinâmico
- Cache de assets estáticos
