from .Model import Model
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING


class Grupo(Model):

    __tablename__ = 'grupos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True)