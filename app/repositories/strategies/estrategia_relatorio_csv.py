from .estrategia_relatorio import RelatorioStrategy

class RelatorioCsvStrategy(RelatorioStrategy):
    def gerar_relatorio(self, dados: str):
        print(f"Gerando relatório em CSV com os dados: {dados}")
        # Lógica de exportação para CSV