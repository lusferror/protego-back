from .Model import Model
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Area import Area
    from .Producto import Producto


class TiempoArea(Model):

    __tablename__ = 'tiempos_area'

    _agregar_atributos = ['tiempo_horas', 'area_nombre', 'producto_codigo', 'tiempo_minutos', 'tiempo_estimado']

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tiempos: Mapped[int] = mapped_column(Integer, nullable=False, comment='Tiempo en segundos que se demora el Area en realizar una actividad')
    area_id: Mapped[int] = mapped_column(Integer, ForeignKey('areas.id'), nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, ForeignKey('productos.id'), nullable=False)
    
    #Relaciones
    area: Mapped['Area'] = relationship('Area')
    producto: Mapped['Producto'] = relationship('Producto')
    
    def tiempo_horas(self):
        return self.tiempos / 3600
    
    def tiempo_minutos(self):
        minutos = self.tiempo_horas() - int(self.tiempo_horas())
        return minutos * 60
    
    def tiempo_estimado(self):
        return f'{str(int(self.tiempo_horas())).zfill(2)}:{str(int(self.tiempo_minutos())).zfill(2)}'

    def area_nombre(self):
        return self.area.nombre
    
    def producto_codigo(self):
        return self.producto.codigo