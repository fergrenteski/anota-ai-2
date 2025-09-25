import csv
from .estrategia_relatorio import RelatorioStrategy

class RelatorioCsvStrategy(RelatorioStrategy):
    """Estratégia para gerar relatórios em CSV."""
    
    def gerar_relatorio(self, dados):
        """Gera um relatório em formato CSV."""
        if not dados:
            print("Nenhum dado fornecido para o relatório")
            return
            
        nome_arquivo = "relatorio.csv"
        
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.DictWriter(arquivo, fieldnames=dados[0].keys())
            writer.writeheader()
            writer.writerows(dados)
        
        print(f"Relatório CSV gerado: {nome_arquivo}")