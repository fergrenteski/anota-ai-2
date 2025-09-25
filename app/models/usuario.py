from app.models.base_model import BaseModel
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Usuario(BaseModel):
    """Modelo de usuário com padrão Memento para histórico de alterações"""
    
    __tablename__ = 'usuarios'
    
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    data_nascimento = db.Column(db.Date)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    
    def __init__(self, nome, email, senha, data_nascimento=None, telefone=None, endereco=None):
        self.nome = nome
        self.email = email
        self.set_senha(senha)
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.endereco = endereco
        self.ativo = True
    
    def set_senha(self, senha):
        """Define a senha do usuário com hash"""
        self.senha_hash = generate_password_hash(senha)
    
    def check_senha(self, senha):
        """Verifica se a senha está correta"""
        return check_password_hash(self.senha_hash, senha)
    
    # Métodos para o padrão Memento
    def criar_memento(self):
        """Cria um memento com o estado atual do usuário"""
        # Import local para evitar dependência circular
        from app.models.usuario_memento import UsuarioMemento
        
        return UsuarioMemento(
            nome=self.nome,
            email=self.email,
            data_nascimento=self.data_nascimento,
            telefone=self.telefone,
            endereco=self.endereco,
            ativo=self.ativo,
            timestamp=datetime.now()
        )
    
    def restaurar_memento(self, memento):
        """
        Restaura o estado do usuário a partir de um memento
        
        Args:
            memento (UsuarioMemento): Memento com o estado a ser restaurado
        """
        self.nome = memento.nome
        self.email = memento.email
        self.data_nascimento = memento.data_nascimento
        self.telefone = memento.telefone
        self.endereco = memento.endereco
        self.ativo = memento.ativo
        
        # Atualiza o timestamp de modificação
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Converte o modelo para dicionário (sem a senha)"""
        data = super().to_dict()
        data.pop('senha_hash', None)
        return data

