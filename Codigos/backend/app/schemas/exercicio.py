"""
@file exercicio.py
@brief Define os schemas Pydantic para a entidade Exercicio, usados para validação de dados.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import uuid
from typing import Optional
from pydantic import BaseModel

class ExercicioBase(BaseModel):
    """Schema base que define os campos comuns de um exercício.

    Serve como classe pai para outros schemas de exercício, evitando repetição de código.

    Attributes:
        nome (str): O nome do exercício (ex: "squat", "push_up").
        descricao (Optional[str]): Uma breve descrição do exercício.
        instrucoes (Optional[str]): Instruções detalhadas sobre como executar o exercício.
    """
    nome: str
    descricao: Optional[str] = None
    instrucoes: Optional[str] = None

class ExercicioCreate(ExercicioBase):
    """Schema usado para validar os dados ao criar um novo exercício.

    Herda todos os campos de ExercicioBase.
    """
    pass

class ExercicioUpdate(ExercicioBase):
    """Schema usado para validar os dados ao atualizar um exercício existente.

    Herda de ExercicioBase, e por padrão do Pydantic, todos os campos
    são opcionais em uma operação de atualização.
    """
    pass

class Exercicio(ExercicioBase):
    """Schema usado para representar um exercício lido da base de dados.

    Inclui todos os campos do ExercicioBase e adiciona o ID único do exercício,
    que é gerado pela base de dados.

    Attributes:
        id (uuid.UUID): ID único do exercício no formato UUID.
    """
    id: uuid.UUID

    class Config:
        """Configuração do Pydantic para o schema.

        'from_attributes = True' permite que o modelo Pydantic seja criado
        a partir dos atributos de um objeto ORM (SQLAlchemy).
        """
        from_attributes = True
