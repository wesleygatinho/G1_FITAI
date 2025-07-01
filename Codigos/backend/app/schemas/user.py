"""
@file user.py
@brief Define os schemas Pydantic para a entidade User, usados para validação de dados.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import uuid
from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """Schema base que define os campos comuns e editáveis de um utilizador.

    Attributes:
        email (EmailStr): E-mail do utilizador, usado para login e comunicação.
        nome (Optional[str]): Nome completo do utilizador.
        data_nascimento (Optional[date]): Data de nascimento do utilizador.
        altura_cm (Optional[float]): Altura do utilizador em centímetros.
        peso_kg (Optional[float]): Peso do utilizador em quilogramas.
        sexo (Optional[str]): Sexo biológico ou género do utilizador.
    """
    email: EmailStr
    nome: Optional[str] = None
    data_nascimento: Optional[date] = None
    altura_cm: Optional[float] = None
    peso_kg: Optional[float] = None
    sexo: Optional[str] = None

class UserCreate(UserBase):
    """Schema para validar os dados ao criar um novo utilizador.

    Herda os campos de UserBase e adiciona o campo de senha,
    que é obrigatório apenas no momento do registo.

    Attributes:
        password (str): Senha do utilizador. Será processada para gerar um hash antes de ser guardada.
    """
    password: str

class UserUpdate(UserBase):
    """Schema para validar os dados ao atualizar um utilizador existente.

    Herda de UserBase. Todos os campos são opcionais, permitindo
    atualizações parciais dos dados do utilizador.
    """
    pass

class UserInDBBase(UserBase):
    """Schema base para representar um utilizador lido da base de dados.

    Inclui campos que são gerados e controlados pelo sistema,
    como ID e flags de estado. Não inclui a senha.

    Attributes:
        id (uuid.UUID): ID único do utilizador no formato UUID.
        is_active (bool): Flag que indica se o utilizador está ativo.
        is_superuser (bool): Flag que indica se o utilizador tem permissões de administrador.
        is_verified (bool): Flag que indica se o e-mail do utilizador foi verificado.
    """
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    is_verified: bool
    
    class Config:
        """Configuração do Pydantic para o schema."""
        # Permite que o Pydantic leia dados diretamente de modelos SQLAlchemy
        orm_mode = True

class User(UserInDBBase):
    """Schema principal usado para retornar os dados de um utilizador na API.

    Este é o modelo de dados que será serializado e enviado como resposta
    em endpoints que retornam informações de um utilizador.
    """
    pass
