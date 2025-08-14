from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from app import db

class BaseModel(db.Model):
    """Classe base para todos os modelos"""
    
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    def save(self):
        """Salva o modelo no banco de dados"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Remove o modelo do banco de dados"""
        db.session.delete(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """Atualiza os campos do modelo"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return self
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
