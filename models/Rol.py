from .Model import Model, db
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    # from .RolUser import RolUser
    from .Usuario import Usuario

class Rol(Model):
    __tablename__ = 'roles'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    descripcion:Mapped[str] = mapped_column(String(50), nullable=False)
    nombre:Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)

    # Relaciones
    usuarios:Mapped[List['Usuario']] = relationship('Usuario',secondary='roles_usuarios', overlaps='roles,roles_usuario')
    