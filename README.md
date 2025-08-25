# Anota-ai

Sistema de anotações desenvolvido em Python com Flask.

# 📱 Anota-aí - Sistema de Controle Financeiro Pessoal

O **Anota-aí** é uma aplicação web completa para controle de finanças pessoais, desenvolvida em Python com Flask. O sistema permite o gerenciamento de despesas e receitas, categorização de gastos, visualização de relatórios e dicas financeiras personalizadas.

## ✨ Funcionalidades

### 🔐 Autenticação e Perfil
- Registro e login de usuários
- Gerenciamento de perfil pessoal
- Alteração de senha
- Desativação de conta

### 💰 Controle Financeiro
- Registro de despesas e receitas
- Categorização automática e personalizada
- Dashboard com resumo financeiro
- Comparação mensal de gastos

### 📊 Relatórios e Análises
- Relatórios diários, semanais e mensais
- Gráficos de tendências
- Análise por categorias
- Estatísticas de uso

### 💡 Dicas Financeiras
- Dicas personalizadas baseadas no perfil
- Categorização por tipo (economia, investimento, organização, educação)
- Sistema de busca de dicas
- Conteúdo educativo

### 🔍 Recursos Adicionais
- Sistema de busca global
- Interface responsiva
- API REST completa
- Validações robustas

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas bem definida:

```
app/
├── controllers/     # Controladores (lógica de apresentação)
├── services/        # Serviços (lógica de negócio)
├── repositories/    # Repositórios (acesso a dados)
├── models/          # Modelos de dados (SQLAlchemy)
├── routes/          # Definição de rotas
├── templates/       # Templates HTML (Jinja2)
└── static/          # Arquivos estáticos (CSS, JS, imagens)
```

### 🧩 Padrões Utilizados
- **MVC (Model-View-Controller)**: Separação clara de responsabilidades
- **Repository Pattern**: Abstração do acesso a dados
- **Service Layer**: Centralização da lógica de negócio
- **Dependency Injection**: Injeção de dependências nos controladores

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd Anota-ai
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente (opcional)
Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///data/anota_ai.db
FLASK_ENV=development
```

### 5. Inicialize o banco de dados
```bash
python init_db.py
```

### 6. Execute a aplicação
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5001`

## 👤 Usuário Demo

Após executar o script de inicialização, você pode usar as seguintes credenciais para testar:

- **Email**: `demo@anotaai.com`
- **Senha**: `demo123`

Este usuário já possui:
- Categorias pré-configuradas
- Despesas e receitas de exemplo
- Dados para visualização nos relatórios

## 📚 Dependências Principais

- **Flask**: Framework web principal
- **SQLAlchemy**: ORM para banco de dados
- **Flask-Login**: Gerenciamento de sessões
- **Flask-Migrate**: Migrações de banco
- **Werkzeug**: Utilitários e segurança
- **Jinja2**: Engine de templates

## 🔧 Desenvolvimento

### Estrutura de Dados

#### Usuário
```python
- id: Integer (PK)
- nome: String(100)
- email: String(120) UNIQUE
- password_hash: String(128)
- telefone: String(20)
- data_nascimento: Date
- profissao: String(100)
- salario: Float
- avatar: String(200)
- data_criacao: DateTime
- ativo: Boolean
```

#### Categoria
```python
- id: Integer (PK)
- nome: String(100)
- descricao: Text
- cor: String(7) # Hexadecimal
- icone: String(50) # FontAwesome
- ativa: Boolean
- usuario_id: Integer (FK)
```

#### Despesa/Receita
```python
- id: Integer (PK)
- descricao: String(200)
- valor: Float
- data: Date
- tipo: Enum (despesa/receita)
- observacoes: Text
- usuario_id: Integer (FK)
- categoria_id: Integer (FK)
```

### API Endpoints

#### Autenticação
- `POST /login` - Login do usuário
- `POST /register` - Registro de novo usuário
- `GET /logout` - Logout

#### Categorias
- `GET /categorias` - Listar categorias
- `POST /categorias/create` - Criar categoria
- `POST /categorias/{id}/update` - Atualizar categoria
- `POST /categorias/{id}/delete` - Excluir categoria

#### Despesas
- `GET /despesas-receitas` - Listar despesas/receitas
- `POST /despesas/create` - Criar despesa/receita
- `POST /despesas/{id}/update` - Atualizar despesa/receita
- `POST /despesas/{id}/delete` - Excluir despesa/receita

#### Dicas
- `GET /dicas` - Listar dicas
- `GET /api/dicas/random` - Dicas aleatórias
- `GET /api/dicas/search?q={termo}` - Buscar dicas
- `GET /api/dicas/personalized` - Dicas personalizadas

## 🧪 Testes

Para executar os testes:
```bash
# Testes unitários
python -m pytest tests/unit/

# Testes de integração
python -m pytest tests/integration/

# Todos os testes
python -m pytest
```

## 📝 Novas Funcionalidades

### Adições Recentes
- ✅ Sistema completo de autenticação
- ✅ Gerenciamento de categorias personalizadas
- ✅ Dashboard com gráficos e estatísticas
- ✅ Sistema de dicas financeiras
- ✅ Relatórios detalhados
- ✅ API REST completa
- ✅ Validações robustas
- ✅ Arquitetura em camadas

### Próximos Passos
- [ ] Sistema de metas financeiras
- [ ] Integração com bancos (Open Banking)
- [ ] Notificações e lembretes
- [ ] Exportação de relatórios (PDF/Excel)
- [ ] Aplicativo móvel
- [ ] Sistema de backup automático

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte:
- Abra uma issue no GitHub
- Entre em contato através do email de suporte

---

**Anota-aí** - Desenvolvido com ❤️ para facilitar o controle de suas finanças pessoais.

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
