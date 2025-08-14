from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from flask import current_app

class BaseService(ABC):
    """Classe base para todos os serviços"""
    
    def __init__(self, repository):
        self.repository = repository
        self.logger = current_app.logger if current_app else None
    
    def create(self, data: Dict) -> Any:
        """Cria um novo registro"""
        try:
            self._validate_create_data(data)
            processed_data = self._process_create_data(data)
            result = self.repository.create(**processed_data)
            self._log_action('CREATE', result.id if hasattr(result, 'id') else 'unknown')
            return result
        except Exception as e:
            self._log_error('CREATE', str(e))
            raise e
    
    def get_by_id(self, id: int) -> Optional[Any]:
        """Busca um registro pelo ID"""
        try:
            result = self.repository.get_by_id(id)
            if not result:
                self._log_warning('GET_BY_ID', f'Registro com ID {id} não encontrado')
            return result
        except Exception as e:
            self._log_error('GET_BY_ID', str(e))
            raise e
    
    def get_all(self, page: int = None, per_page: int = None) -> List[Any]:
        """Retorna todos os registros"""
        try:
            return self.repository.get_all(page=page, per_page=per_page)
        except Exception as e:
            self._log_error('GET_ALL', str(e))
            raise e
    
    def update(self, id: int, data: Dict) -> Optional[Any]:
        """Atualiza um registro"""
        try:
            instance = self.repository.get_by_id(id)
            if not instance:
                self._log_warning('UPDATE', f'Registro com ID {id} não encontrado')
                return None
            
            self._validate_update_data(data)
            processed_data = self._process_update_data(data)
            result = self.repository.update(instance, **processed_data)
            self._log_action('UPDATE', id)
            return result
        except Exception as e:
            self._log_error('UPDATE', str(e))
            raise e
    
    def delete(self, id: int) -> bool:
        """Deleta um registro"""
        try:
            instance = self.repository.get_by_id(id)
            if not instance:
                self._log_warning('DELETE', f'Registro com ID {id} não encontrado')
                return False
            
            success = self.repository.delete(instance)
            if success:
                self._log_action('DELETE', id)
            return success
        except Exception as e:
            self._log_error('DELETE', str(e))
            raise e
    
    def get_paginated(self, page: int = 1, per_page: int = 10, **filters):
        """Retorna registros paginados"""
        try:
            return self.repository.get_paginated(page=page, per_page=per_page, **filters)
        except Exception as e:
            self._log_error('GET_PAGINATED', str(e))
            raise e
    
    def count(self) -> int:
        """Retorna a contagem total de registros"""
        try:
            return self.repository.count()
        except Exception as e:
            self._log_error('COUNT', str(e))
            raise e
    
    # Métodos para serem implementados pelas classes filhas
    def _validate_create_data(self, data: Dict) -> None:
        """Valida os dados para criação (implementar nas classes filhas)"""
        pass
    
    def _validate_update_data(self, data: Dict) -> None:
        """Valida os dados para atualização (implementar nas classes filhas)"""
        pass
    
    def _process_create_data(self, data: Dict) -> Dict:
        """Processa os dados antes da criação (implementar nas classes filhas)"""
        return data
    
    def _process_update_data(self, data: Dict) -> Dict:
        """Processa os dados antes da atualização (implementar nas classes filhas)"""
        return data
    
    # Métodos de logging
    def _log_action(self, action: str, id: Any) -> None:
        """Log de ação realizada"""
        if self.logger:
            self.logger.info(f'{self.__class__.__name__}: {action} - ID: {id}')
    
    def _log_error(self, action: str, error: str) -> None:
        """Log de erro"""
        if self.logger:
            self.logger.error(f'{self.__class__.__name__}: {action} - Erro: {error}')
    
    def _log_warning(self, action: str, message: str) -> None:
        """Log de aviso"""
        if self.logger:
            self.logger.warning(f'{self.__class__.__name__}: {action} - {message}')
