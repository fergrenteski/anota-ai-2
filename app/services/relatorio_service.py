from app.repositories.strategies.estrategia_relatorio import RelatorioStrategy

class RelatoriosService:
    def __init__(self):
        self._strategy: RelatorioStrategy | None = None

    def set_strategy(self, strategy: RelatorioStrategy):
        self._strategy = strategy

    def gerar(self, dados: str):
        if not self._strategy:
            raise ValueError("Nenhuma estratégia de relatório definida!")
        self._strategy.gerar_relatorio(dados)