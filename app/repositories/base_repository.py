from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from flask_sqlalchemy import SQLAlchemy
from app import db

class BaseRepository(ABC):
    """Classe base para todos os repositórios"""
    
    def __init__(self, model):
        self.model = model
    
    def create(self, **kwargs) -> Any:
        """Cria um novo registro"""
        try:
            instance = self.model(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_by_id(self, id: int) -> Optional[Any]:
        """Busca um registro pelo ID"""
        return self.model.query.get(id)
    
    def get_all(self, page: int = None, per_page: int = None) -> List[Any]:
        """Retorna todos os registros com paginação opcional"""
        query = self.model.query
        if page and per_page:
            return query.paginate(page=page, per_page=per_page, error_out=False).items
        return query.all()
    
    def update(self, instance: Any, **kwargs) -> Any:
        """Atualiza um registro"""
        try:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self, instance: Any) -> bool:
        """Deleta um registro"""
        try:
            db.session.delete(instance)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    
    def delete_by_id(self, id: int) -> bool:
        """Deleta um registro pelo ID"""
        instance = self.get_by_id(id)
        if instance:
            return self.delete(instance)
        return False
    
    def get_by_field(self, field: str, value: Any) -> Optional[Any]:
        """Busca um registro por um campo específico"""
        return self.model.query.filter(getattr(self.model, field) == value).first()
    
    def filter_by(self, **kwargs) -> List[Any]:
        """Filtra registros por campos específicos"""
        return self.model.query.filter_by(**kwargs).all()
    
    def count(self) -> int:
        """Retorna a contagem total de registros"""
        return self.model.query.count()
    
    def exists(self, **kwargs) -> bool:
        """Verifica se existe um registro com os critérios especificados"""
        return self.model.query.filter_by(**kwargs).first() is not None
    
    def get_paginated(self, page: int = 1, per_page: int = 10, **filters):
        """Retorna registros paginados com filtros opcionais"""
        query = self.model.query
        if filters:
            query = query.filter_by(**filters)
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    def bulk_create(self, data_list: List[Dict]) -> List[Any]:
        """Cria múltiplos registros em uma única transação"""
        try:
            instances = [self.model(**data) for data in data_list]
            db.session.add_all(instances)
            db.session.commit()
            return instances
        except Exception as e:
            db.session.rollback()
            raise e
