from .Model import Model, db
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Rol import Rol
    from .Usuario import Usuario

class RolUsuario(Model):
    __tablename__ = 'roles_usuarios'

    usuario_id:Mapped[int] = mapped_column(Integer, ForeignKey('usuarios.id'), nullable=False, primary_key=True)
    rol_id:Mapped[int] = mapped_column(Integer, ForeignKey('roles.id'), nullable=False, primary_key=True)
    activo:Mapped[bool] = mapped_column(Boolean, default=True)

    # Relaciones
    usuarios:Mapped['Rol'] = relationship('Usuario', overlaps='roles, usuarios, roles_usuario')
    roles:Mapped['Usuario'] = relationship('Rol', overlaps='roles, usuarios')


