from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()

# ===== USUÁRIO FICTÍCIO =====
class UsuarioFicticio:
    def __init__(self, id, email, nome):
        self.id = id
        self.email = email
        self.nome = nome
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return str(self.id)

# Usuário demo para login
USUARIO_DEMO = UsuarioFicticio(1, 'demo@anotaai.com', 'Usuário Demo')

def create_app():
    app = Flask(__name__)
    
    # Configuração mínima necessária
    app.config['SECRET_KEY'] = 'demo-secret-key-ficticio'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Configure Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        if user_id == '1':
            return USUARIO_DEMO
        return None

    # Register blueprints
    from app.routes import main_bp
    from app.routes.dashboard_api import dashboard_api
    
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_api)

    return app