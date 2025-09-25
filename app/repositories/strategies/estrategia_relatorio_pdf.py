from .estrategia_relatorio import RelatorioStrategy

class RelatorioPdfStrategy(RelatorioStrategy):
    def gerar_relatorio(self, dados: str):
        print(f"Gerando relatório em PDF com os dados: {dados}")
        # Aqui entraria a lógica real de exportação para PDF