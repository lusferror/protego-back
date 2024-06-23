from .Model import Model
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Orden import Orden

class Cliente(Model):

    __tablename__ = 'clientes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    rut: Mapped[str] = mapped_column(String(12), unique=True, nullable=False, index=True)
    direccion: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[str] = mapped_column(String(12), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relaciones
    ordenes: Mapped[List['Orden']] = relationship('Orden')
 