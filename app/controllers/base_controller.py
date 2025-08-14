from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from flask import request, jsonify, render_template, flash, redirect, url_for
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

class BaseController(ABC):
    """Classe base para todos os controladores"""
    
    def __init__(self, service):
        self.service = service
    
    def index(self):
        """Lista todos os registros (GET /)"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            if self._is_api_request():
                items = self.service.get_all(page=page, per_page=per_page)
                return self._api_response([item.to_dict() if hasattr(item, 'to_dict') else str(item) for item in items])
            else:
                pagination = self.service.get_paginated(page=page, per_page=per_page)
                return self._render_template('index.html', pagination=pagination)
        except Exception as e:
            return self._handle_error(e, 'Erro ao listar registros')
    
    def show(self, id: int):
        """Mostra um registro específico (GET /<id>)"""
        try:
            item = self.service.get_by_id(id)
            if not item:
                return self._handle_not_found()
            
            if self._is_api_request():
                return self._api_response(item.to_dict() if hasattr(item, 'to_dict') else str(item))
            else:
                return self._render_template('show.html', item=item)
        except Exception as e:
            return self._handle_error(e, f'Erro ao buscar registro {id}')
    
    def create(self):
        """Cria um novo registro (POST /)"""
        try:
            data = self._get_request_data()
            self._validate_create_data(data)
            
            item = self.service.create(data)
            
            if self._is_api_request():
                return self._api_response(
                    item.to_dict() if hasattr(item, 'to_dict') else str(item),
                    status_code=201
                )
            else:
                flash('Registro criado com sucesso!', 'success')
                return redirect(url_for(f'{self._get_blueprint_name()}.show', id=item.id))
        except Exception as e:
            return self._handle_error(e, 'Erro ao criar registro')
    
    def update(self, id: int):
        """Atualiza um registro (PUT/PATCH /<id>)"""
        try:
            data = self._get_request_data()
            self._validate_update_data(data)
            
            item = self.service.update(id, data)
            if not item:
                return self._handle_not_found()
            
            if self._is_api_request():
                return self._api_response(item.to_dict() if hasattr(item, 'to_dict') else str(item))
            else:
                flash('Registro atualizado com sucesso!', 'success')
                return redirect(url_for(f'{self._get_blueprint_name()}.show', id=id))
        except Exception as e:
            return self._handle_error(e, f'Erro ao atualizar registro {id}')
    
    def delete(self, id: int):
        """Deleta um registro (DELETE /<id>)"""
        try:
            success = self.service.delete(id)
            if not success:
                return self._handle_not_found()
            
            if self._is_api_request():
                return self._api_response({'message': 'Registro deletado com sucesso'})
            else:
                flash('Registro deletado com sucesso!', 'success')
                return redirect(url_for(f'{self._get_blueprint_name()}.index'))
        except Exception as e:
            return self._handle_error(e, f'Erro ao deletar registro {id}')
    
    def new(self):
        """Exibe formulário para criar novo registro (GET /new)"""
        if self._is_api_request():
            return self._api_response({'error': 'Endpoint não disponível para API'}, status_code=404)
        return self._render_template('new.html')
    
    def edit(self, id: int):
        """Exibe formulário para editar registro (GET /<id>/edit)"""
        try:
            if self._is_api_request():
                return self._api_response({'error': 'Endpoint não disponível para API'}, status_code=404)
            
            item = self.service.get_by_id(id)
            if not item:
                return self._handle_not_found()
            
            return self._render_template('edit.html', item=item)
        except Exception as e:
            return self._handle_error(e, f'Erro ao buscar registro {id} para edição')
    
    # Métodos auxiliares
    def _is_api_request(self) -> bool:
        """Verifica se é uma requisição para API"""
        return (
            request.is_json or 
            'application/json' in request.headers.get('Accept', '') or
            request.path.startswith('/api/')
        )
    
    def _get_request_data(self) -> Dict:
        """Extrai dados da requisição"""
        if request.is_json:
            return request.get_json() or {}
        return request.form.to_dict()
    
    def _api_response(self, data: Any, status_code: int = 200) -> Any:
        """Retorna resposta para API"""
        return jsonify(data), status_code
    
    def _render_template(self, template: str, **kwargs) -> str:
        """Renderiza template com dados"""
        template_path = f'{self._get_template_folder()}/{template}'
        return render_template(template_path, **kwargs)
    
    def _handle_error(self, error: Exception, message: str = 'Erro interno') -> Any:
        """Trata erros da aplicação"""
        if self._is_api_request():
            return self._api_response({
                'error': message,
                'details': str(error)
            }, status_code=500)
        else:
            flash(message, 'error')
            return redirect(url_for(f'{self._get_blueprint_name()}.index'))
    
    def _handle_not_found(self) -> Any:
        """Trata erro 404"""
        if self._is_api_request():
            return self._api_response({'error': 'Registro não encontrado'}, status_code=404)
        else:
            flash('Registro não encontrado', 'error')
            return redirect(url_for(f'{self._get_blueprint_name()}.index'))
    
    # Métodos para serem implementados pelas classes filhas
    @abstractmethod
    def _get_blueprint_name(self) -> str:
        """Retorna o nome do blueprint (implementar nas classes filhas)"""
        pass
    
    @abstractmethod
    def _get_template_folder(self) -> str:
        """Retorna a pasta dos templates (implementar nas classes filhas)"""
        pass
    
    def _validate_create_data(self, data: Dict) -> None:
        """Valida dados para criação (implementar nas classes filhas se necessário)"""
        pass
    
    def _validate_update_data(self, data: Dict) -> None:
        """Valida dados para atualização (implementar nas classes filhas se necessário)"""
        pass
