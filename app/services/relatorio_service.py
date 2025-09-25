from app.repositories.strategies.estrategia_relatorio import RelatorioStrategy

class RelatoriosService:
    """Serviço para geração de relatórios usando o padrão Strategy."""
    
    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy: RelatorioStrategy):
        """Define a estratégia de geração de relatório."""
        self._strategy = strategy

    def gerar(self, dados):
        """Gera um relatório usando a estratégia definida."""
        if not self._strategy:
            print("Nenhuma estratégia de relatório definida!")
            return
        
        self._strategy.gerar_relatorio(dados)