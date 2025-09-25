from typing import List, Optional
from app.models.usuario_memento import UsuarioMemento


class CaretakerUsuario:
    """
    Caretaker que gerencia os mementos do usuário
    
    Responsável por:
    - Armazenar histórico de mementos
    - Gerenciar operações de undo/redo
    - Controlar navegação pelo histórico
    """
    
    def __init__(self, max_historico: int = 50):
        """
        Inicializa o caretaker
        
        Args:
            max_historico (int): Número máximo de mementos no histórico
        """
        self._historico: List[UsuarioMemento] = []
        self._indice_atual: int = -1
        self._max_historico: int = max_historico
    
    def salvar_estado(self, usuario) -> None:
        """
        Salva o estado atual do usuário
        
        Args:
            usuario: Instância do usuário para salvar o estado
        """
        memento = usuario.criar_memento()
        
        # Se estamos no meio do histórico (após undo), remove estados futuros
        if self._indice_atual < len(self._historico) - 1:
            self._historico = self._historico[:self._indice_atual + 1]
        
        # Adiciona o novo memento
        self._historico.append(memento)
        self._indice_atual += 1
        
        # Limita o tamanho do histórico
        self._limitar_historico()
    
    def desfazer(self, usuario) -> bool:
        """
        Desfaz a última alteração (undo)
        
        Args:
            usuario: Instância do usuário para restaurar
            
        Returns:
            bool: True se conseguiu desfazer, False caso contrário
        """
        if not self.pode_desfazer():
            return False
        
        self._indice_atual -= 1
        memento = self._historico[self._indice_atual]
        usuario.restaurar_memento(memento)
        return True
    
    def refazer(self, usuario) -> bool:
        """
        Refaz uma alteração desfeita (redo)
        
        Args:
            usuario: Instância do usuário para restaurar
            
        Returns:
            bool: True se conseguiu refazer, False caso contrário
        """
        if not self.pode_refazer():
            return False
        
        self._indice_atual += 1
        memento = self._historico[self._indice_atual]
        usuario.restaurar_memento(memento)
        return True
    
    def obter_historico(self) -> List[UsuarioMemento]:
        """
        Retorna o histórico de alterações
        
        Returns:
            List[UsuarioMemento]: Lista com todos os mementos do histórico
        """
        return self._historico.copy()
    
    def obter_memento_atual(self) -> Optional[UsuarioMemento]:
        """
        Retorna o memento atual (onde estamos no histórico)
        
        Returns:
            UsuarioMemento: Memento atual ou None se histórico vazio
        """
        if self._indice_atual >= 0 and self._indice_atual < len(self._historico):
            return self._historico[self._indice_atual]
        return None
    
    def limpar_historico(self) -> None:
        """Limpa todo o histórico"""
        self._historico.clear()
        self._indice_atual = -1
    
    def pode_desfazer(self) -> bool:
        """
        Verifica se é possível desfazer
        
        Returns:
            bool: True se pode desfazer, False caso contrário
        """
        return self._indice_atual > 0
    
    def pode_refazer(self) -> bool:
        """
        Verifica se é possível refazer
        
        Returns:
            bool: True se pode refazer, False caso contrário
        """
        return self._indice_atual < len(self._historico) - 1
    
    def obter_tamanho_historico(self) -> int:
        """
        Retorna o número de itens no histórico
        
        Returns:
            int: Número de mementos no histórico
        """
        return len(self._historico)
    
    def obter_indice_atual(self) -> int:
        """
        Retorna o índice atual no histórico
        
        Returns:
            int: Índice atual no histórico
        """
        return self._indice_atual
    
    def navegar_para(self, indice: int, usuario) -> bool:
        """
        Navega diretamente para um índice específico no histórico
        
        Args:
            indice (int): Índice para navegar
            usuario: Instância do usuário para restaurar
            
        Returns:
            bool: True se conseguiu navegar, False caso contrário
        """
        if 0 <= indice < len(self._historico):
            self._indice_atual = indice
            memento = self._historico[self._indice_atual]
            usuario.restaurar_memento(memento)
            return True
        return False
    
    def _limitar_historico(self) -> None:
        """Limita o histórico ao tamanho máximo configurado"""
        if len(self._historico) > self._max_historico:
            # Remove os mementos mais antigos
            excesso = len(self._historico) - self._max_historico
            self._historico = self._historico[excesso:]
            self._indice_atual -= excesso
            
            # Garante que o índice não fique negativo
            if self._indice_atual < 0:
                self._indice_atual = 0
    
    def obter_estatisticas(self) -> dict:
        """
        Retorna estatísticas do histórico
        
        Returns:
            dict: Dicionário com estatísticas do caretaker
        """
        return {
            'total_mementos': len(self._historico),
            'indice_atual': self._indice_atual,
            'pode_desfazer': self.pode_desfazer(),
            'pode_refazer': self.pode_refazer(),
            'max_historico': self._max_historico,
            'primeiro_memento': self._historico[0].timestamp if self._historico else None,
            'ultimo_memento': self._historico[-1].timestamp if self._historico else None,
            'memento_atual': self.obter_memento_atual().timestamp if self.obter_memento_atual() else None
        }
    
    def __str__(self) -> str:
        """Representação string do caretaker"""
        return f"CaretakerUsuario(historico={len(self._historico)}, atual={self._indice_atual})"
    
    def __repr__(self) -> str:
        """Representação para debug"""
        return self.__str__()