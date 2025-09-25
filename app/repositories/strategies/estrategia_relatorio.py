from abc import ABC, abstractmethod

class RelatorioStrategy(ABC):
    """Interface Strategy para geração de relatórios."""
    
    @abstractmethod
    def gerar_relatorio(self, dados):
        """Gera um relatório com os dados fornecidos."""
        pass