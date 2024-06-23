from .Model import Model
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

class Tamano(Model):

    __tablename__ = 'tamanos'

    _agregar_atributos = ['nombre_tamano']

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    largo: Mapped[int] = mapped_column(Integer, nullable=False)
    ancho: Mapped[int] = mapped_column(Integer, nullable=False)
    alto: Mapped[int] = mapped_column(Integer, nullable=False)

    def nombre_tamano(self) -> str:
        return f"{self.largo}x{self.ancho}x{self.alto}"