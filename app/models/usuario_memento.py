from datetime import datetime


class UsuarioMemento:
    """Memento que armazena o estado do usuário em um momento específico"""
    
    def __init__(self, nome, email, data_nascimento=None, telefone=None, 
                 endereco=None, ativo=True, timestamp=None):
        """
        Inicializa um memento com o estado do usuário
        
        Args:
            nome (str): Nome do usuário
            email (str): Email do usuário
            data_nascimento (date): Data de nascimento
            telefone (str): Telefone do usuário
            endereco (str): Endereço do usuário
            ativo (bool): Status ativo/inativo
            timestamp (datetime): Momento da criação do memento
        """
        self._nome = nome
        self._email = email
        self._data_nascimento = data_nascimento
        self._telefone = telefone
        self._endereco = endereco
        self._ativo = ativo
        self._timestamp = timestamp or datetime.now()
    
    # Getters para acessar o estado armazenado (somente leitura)
    @property
    def nome(self):
        """Retorna o nome armazenado no memento"""
        return self._nome
    
    @property
    def email(self):
        """Retorna o email armazenado no memento"""
        return self._email
    
    @property
    def data_nascimento(self):
        """Retorna a data de nascimento armazenada no memento"""
        return self._data_nascimento
    
    @property
    def telefone(self):
        """Retorna o telefone armazenado no memento"""
        return self._telefone
    
    @property
    def endereco(self):
        """Retorna o endereço armazenado no memento"""
        return self._endereco
    
    @property
    def ativo(self):
        """Retorna o status ativo armazenado no memento"""
        return self._ativo
    
    @property
    def timestamp(self):
        """Retorna o timestamp de criação do memento"""
        return self._timestamp
    
    def to_dict(self):
        """Converte o memento para dicionário"""
        return {
            'nome': self._nome,
            'email': self._email,
            'data_nascimento': self._data_nascimento,
            'telefone': self._telefone,
            'endereco': self._endereco,
            'ativo': self._ativo,
            'timestamp': self._timestamp
        }
    
    def __str__(self):
        """Representação string do memento"""
        return f"UsuarioMemento({self._nome}, {self._email}, {self._timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
    
    def __repr__(self):
        """Representação para debug"""
        return self.__str__()