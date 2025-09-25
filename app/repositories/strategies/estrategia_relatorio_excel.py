from .estrategia_relatorio import RelatorioStrategy

class RelatorioExcelStrategy(RelatorioStrategy):
    """Estratégia para gerar relatórios em Excel."""
    
    def gerar_relatorio(self, dados):
        """Gera um relatório em formato Excel."""
        try:
            import pandas as pd
            
            if not dados:
                print("Nenhum dado fornecido para o relatório")
                return
                
            nome_arquivo = "relatorio.xlsx"
            df = pd.DataFrame(dados)
            df.to_excel(nome_arquivo, index=False)
            
            print(f"Relatório Excel gerado: {nome_arquivo}")
            
        except ImportError:
            print("pandas não está instalado. Instale com: pip install pandas openpyxl")