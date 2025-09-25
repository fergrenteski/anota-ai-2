from app.models.usuario import Usuario
from app.models.caretaker_usuario import CaretakerUsuario
from app.repositories.usuario_repository import UsuarioRepository


class PerfilService:
    """Serviço para gerenciar perfis de usuário com padrão Memento"""
    
    def __init__(self):
        self.usuario_repository = UsuarioRepository()
        self.caretaker = CaretakerUsuario()
    
    def obter_usuario_por_id(self, usuario_id):
        """Obtém um usuário pelo ID"""
        pass
    
    def atualizar_perfil(self, usuario_id, dados_atualizacao):
        """Atualiza o perfil do usuário salvando o estado anterior"""
        pass
    
    def alterar_senha(self, usuario_id, senha_atual, nova_senha):
        """Altera a senha do usuário"""
        pass
    
    def desativar_usuario(self, usuario_id):
        """Desativa um usuário"""
        pass
    
    def ativar_usuario(self, usuario_id):
        """Ativa um usuário"""
        pass
    
    # Métodos relacionados ao padrão Memento
    def desfazer_alteracao(self, usuario_id):
        """Desfaz a última alteração no perfil do usuário"""
        pass
    
    def refazer_alteracao(self, usuario_id):
        """Refaz uma alteração desfeita no perfil"""
        pass
    
    def obter_historico_alteracoes(self, usuario_id):
        """Obtém o histórico de alterações do usuário"""
        pass
    
    def limpar_historico(self, usuario_id):
        """Limpa o histórico de alterações do usuário"""
        pass
    
    def pode_desfazer(self, usuario_id):
        """Verifica se é possível desfazer alterações"""
        pass
    
    def pode_refazer(self, usuario_id):
        """Verifica se é possível refazer alterações"""
        pass