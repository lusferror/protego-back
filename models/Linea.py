from .Model import Model
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Producto import Producto


class Linea(Model):

    __tablename__ = 'lineas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relaciones
    productos: Mapped[List['Producto']] = relationship('Producto', back_populates='linea')
    