from .estrategia_relatorio import RelatorioStrategy

class RelatorioPdfStrategy(RelatorioStrategy):
    """Estratégia para gerar relatórios em PDF."""
    
    def gerar_relatorio(self, dados):
        """Gera um relatório em formato PDF."""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table
            
            if not dados:
                print("Nenhum dado fornecido para o relatório")
                return
                
            nome_arquivo = "relatorio.pdf"
            doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
            
            # Prepara os dados para a tabela
            colunas = list(dados[0].keys())
            dados_tabela = [colunas]
            
            for linha in dados:
                dados_tabela.append([str(linha.get(col, '')) for col in colunas])
            
            # Cria a tabela
            tabela = Table(dados_tabela)
            doc.build([tabela])
            
            print(f"Relatório PDF gerado: {nome_arquivo}")
            
        except ImportError:
            print("reportlab não está instalado. Instale com: pip install reportlab")