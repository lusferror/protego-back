from .Model import Model
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .TipoIncidente import TipoIncidente
    from .Usuario import Usuario
    from .Area import Area

class Incidente(Model):
    
    __tablename__ = 'incidentes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    orden_id: Mapped[int] = mapped_column(Integer, ForeignKey('ordenes.id'),  nullable=False)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey('usuarios.id'), nullable=False, comment='Usuario que reporta el incidente')
    tipo_incidente_id: Mapped[int] = mapped_column(Integer, ForeignKey('tipos_incidentes.id'), nullable=False, comment='Tipo de incidente')
    area_id: Mapped[int] = mapped_column(Integer, ForeignKey('areas.id'), nullable=True, comment='Area donde se reporta el incidente')
    observaciones: Mapped[str] = mapped_column(String(250), nullable=True, comment='Comentarios del incidente')

    # Relaciones
    usuario: Mapped['Usuario'] = relationship('Usuario')
    tipo_incidente: Mapped['TipoIncidente'] = relationship('TipoIncidente')
    area: Mapped['Area'] = relationship('Area')
    

