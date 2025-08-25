# Controladores da aplicação
from .base_controller import BaseController
from .perfil_controller import PerfilController
from .categoria_controller import CategoriaController
from .dicas_controller import DicaController

__all__ = [
    'BaseController',
    'PerfilController',
    'CategoriaController',
    'DicaController'
]
