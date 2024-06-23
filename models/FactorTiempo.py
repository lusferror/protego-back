from .Model import Model
from sqlalchemy import Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Grupo import Grupo

class FactorTiempo(Model):

    _agregar_atributos = ['grupo_nombre']
    
    __tablename__ = 'factores_tiempos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grupo_id: Mapped[int] = mapped_column(Integer, ForeignKey('grupos.id'), nullable=False)
    alto: Mapped[int] = mapped_column(Integer, nullable=False)
    ancho: Mapped[int] = mapped_column(Integer, nullable=False)
    factor: Mapped[float] = mapped_column(Float, nullable=False)

    # Relaciones
    grupo: Mapped['Grupo'] = relationship('Grupo')

    def grupo_nombre(self) -> str:
        return self.grupo.nombre