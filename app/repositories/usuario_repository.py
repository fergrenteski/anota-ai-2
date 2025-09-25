from app.repositories.base_repository import BaseRepository
from app.models.usuario import Usuario


class UsuarioRepository(BaseRepository):
    """Repositório para operações com usuários"""
    
    def __init__(self):
        super().__init__(Usuario)
    
    def buscar_por_email(self, email):
        """Busca um usuário pelo email"""
        pass
    
    def buscar_ativos(self):
        """Retorna todos os usuários ativos"""
        pass
    
    def buscar_inativos(self):
        """Retorna todos os usuários inativos"""
        pass
    
    def email_existe(self, email, excluir_id=None):
        """Verifica se um email já está em uso"""
        pass
    
    def atualizar_senha(self, usuario_id, nova_senha_hash):
        """Atualiza a senha do usuário"""
        pass
    
    def desativar(self, usuario_id):
        """Desativa um usuário"""
        pass
    
    def ativar(self, usuario_id):
        """Ativa um usuário"""
        pass