"""
Módulo de estratégias para geração de relatórios.
Implementa o padrão Strategy para diferentes formatos de relatório.
"""

from .estrategia_relatorio import RelatorioStrategy
from .estrategia_relatorio_csv import RelatorioCsvStrategy
from .estrategia_relatorio_excel import RelatorioExcelStrategy
from .estrategia_relatorio_pdf import RelatorioPdfStrategy

__all__ = [
    'RelatorioStrategy',
    'RelatorioCsvStrategy', 
    'RelatorioExcelStrategy',
    'RelatorioPdfStrategy'
]