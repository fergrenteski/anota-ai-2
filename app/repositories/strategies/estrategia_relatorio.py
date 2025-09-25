from abc import ABC, abstractmethod

class RelatorioStrategy(ABC):
    @abstractmethod
    def gerar_relatorio(self, dados: str):
        """
        Método abstrato para gerar relatórios.
        Deve ser implementado pelas classes concretas.
        """
        pass