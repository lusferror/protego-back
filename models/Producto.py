from .Model import Model
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Linea import Linea
    from .Grupo import Grupo

class Producto(Model):

    _agregar_atributos = ['linea_nombre', 'grupo_nombre']
    
    __tablename__ = 'productos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    linea_id: Mapped[int] = mapped_column(Integer, ForeignKey('lineas.id'))
    grupo_id: Mapped[int] = mapped_column(Integer, ForeignKey('grupos.id'), nullable=True)
    ancho: Mapped[int] = mapped_column(Integer, nullable=True, comment='Ancho en centimetros')
    alto: Mapped[int] = mapped_column(Integer, nullable=True, comment='Alto en centimetros')
    largo: Mapped[int] = mapped_column(Integer, nullable=True, comment='Largo en centimetros')

    # Relaciones
    linea: Mapped['Linea'] = relationship('Linea')
    grupo: Mapped['Grupo'] = relationship('Grupo')

    def linea_nombre(self) -> str:
        return self.linea.nombre

    def grupo_nombre(self) -> str:
        return self.grupo.nombre if self.grupo else ''
