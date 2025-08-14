# Anota-ai

Sistema de anotações desenvolvido em Python com Flask.

## Estrutura do Projeto

```
anota-ai/
├── app/
│   ├── models/          # Modelos de dados (SQLAlchemy)
│   ├── repositories/    # Camada de acesso a dados
│   ├── services/        # Lógica de negócio
│   ├── controllers/     # Controladores
│   ├── routes/          # Rotas da aplicação
│   ├── templates/       # Templates Jinja2
│   ├── static/          # Arquivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── __init__.py
├── config/              # Configurações
├── tests/               # Testes
│   ├── unit/
│   └── integration/
├── docs/                # Documentação
├── data/                # Banco de dados SQLite
├── migrations/          # Migrações do banco
├── requirements.txt
└── app.py
```

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual: `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows)
4. Instale as dependências: `pip install -r requirements.txt`
5. Configure as variáveis de ambiente
6. Execute as migrações: `flask db upgrade`
7. Execute a aplicação: `python app.py`

## Tecnologias

- Python 3.8+
- Flask
- SQLAlchemy
- SQLite
- Jinja2
- HTML/CSS/JavaScript
