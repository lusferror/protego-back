from .Model import Model
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, ForeignKey

if TYPE_CHECKING:
    from .Rol import Rol
    from .Area import Area
    from .RolUsuario import RolUsuario


class Usuario(Model):

    __tablename__ = "usuarios"

    _ocultar = ["password"]

    _agregar_atributos = ["nombre_completo", "area_nombre", "roles_nombres"]

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(25), nullable=False, index=True)
    segundo_nombre: Mapped[str] = mapped_column(String(25), nullable=True)
    apellido: Mapped[str] = mapped_column(String(25), nullable=False, index=True)
    segundo_apellido: Mapped[str] = mapped_column(String(25), nullable=True)
    rut: Mapped[str] = mapped_column(
        String(12), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    password = mapped_column(String(250), nullable=False)
    telefono: Mapped[str] = mapped_column(String(12), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    area_id = mapped_column(Integer, ForeignKey("areas.id"), nullable=True)

    # Relaciones
    roles: Mapped[List["Rol"]] = relationship(
        "Rol",
        secondary="roles_usuarios",
        primaryjoin="and_(Usuario.id==RolUsuario.usuario_id, RolUsuario.activo==True)",
    )
    roles_usuario: Mapped[List["RolUsuario"]] = relationship("RolUsuario", overlaps="roles,roles_usuario")
    area: Mapped["Area"] = relationship("Area")

    def nombre_completo(self):
        return self.nombre + " " + self.apellido
    
    def area_nombre(self):
        return self.area.nombre if self.area else ""
    
    def roles_nombres(self):
        nombre:str = ''
        for rol in self.roles:
            nombre+=rol.nombre+', '
        return nombre
    