from .estrategia_relatorio import RelatorioStrategy

class RelatorioExcelStrategy(RelatorioStrategy):
    def gerar_relatorio(self, dados: str):
        print(f"Gerando relatório em Excel com os dados: {dados}")
        # Lógica de exportação para Excel