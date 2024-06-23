from .Model import Model
from sqlalchemy import Integer, DateTime, desc, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from .Area import Area
    from .Usuario import Usuario
    from .Orden import Orden


class BitacoraOrden(Model):

    __tablename__ = 'bitacora_ordenes'

    _agregar_atributos = [
        'tiempo_real', 
        'tiempo_estimado', 
        'tiempo_estimado_segundos',
        'tiempo_real_segundos'
    ]

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inicio: Mapped[str] = mapped_column(DateTime, nullable=True, comment='Fecha de inicio de la actividad', default=datetime.now())
    fin: Mapped[str] = mapped_column(DateTime, nullable=True, comment='Fecha de fin de la actividad')
    orden_id: Mapped[int] = mapped_column(Integer, ForeignKey('ordenes.id'), nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, ForeignKey('areas.id'), nullable=False)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey('usuarios.id'), nullable=False)

    # Relaciones
    orden: Mapped['Orden'] = relationship('Orden', overlaps='bitacora, bitacora_ultimo')
    area: Mapped['Area'] = relationship('Area')
    usuario: Mapped['Usuario'] = relationship('Usuario')

    """
    Esta función calcula el tiempo real.

    Args:
        string (bool): Si es True, devuelve el tiempo como una cadena. 
                       Si es False, devuelve el tiempo como un objeto timedelta.

    Returns:
        str | timedelta: El tiempo real.
    """
    def tiempo_real(self, string=True) -> str | timedelta:
        if (self.inicio is None or self.fin is None):
            return None
        resultado = self.fin - self.inicio
        if string:
            segundos = int(resultado.total_seconds())
            horas, remanente = divmod(segundos, 3600)
            minutos, segundos = divmod(remanente, 60)
            horas_final = str(horas).zfill(2)
            minutos_final = str(minutos).zfill(2)
            segundos_final = str(segundos).zfill(2)
            return f"{horas_final}:{minutos_final}:{segundos_final}"
        else:
            return resultado
    
    """
    Esta función calcula el tiempo estimado.

    Args:
        string (bool): Si es True, devuelve el tiempo como una cadena. 
                       Si es False, devuelve el tiempo como un objeto timedelta.
                    
    Returns:
        str | timedelta: El tiempo estimado.
    """
    def tiempo_estimado(self, string=True) -> str | timedelta:
        from .TiempoArea import TiempoArea
        from .FactorTiempo import FactorTiempo

        tiempo_area = TiempoArea.query.filter_by(
            producto_id=self.orden.producto_id, area_id=self.area_id).first()
        if tiempo_area is not None:
            tiempo = tiempo_area.tiempos
            tiempo = timedelta(seconds=tiempo)

            factor = FactorTiempo.query.filter_by(
                grupo_id=self.orden.producto.grupo_id).order_by(desc(FactorTiempo.factor)).all()
            if factor is not None:
                for f in factor:
                    if (self.orden.alto >= f.alto or self.orden.ancho >= f.ancho):
                        tiempo = tiempo * (1 + f.factor)
                        break

            if string:
                return str(tiempo)
            else:
                return tiempo
        else:
            return "00:00:00"

    """
    Esta función calcula el tiempo estimado en segundos.
    Returns:
        int: El tiempo estimado en segundos
    """   
    def tiempo_estimado_segundos(self) -> int:
        tiempo = self.tiempo_estimado(string=False)
        if isinstance(tiempo, timedelta):
            return tiempo.total_seconds()
        else:
            return 0

    """
    Esta función calcula el tiempo real en segundos.
    Returns:
        int: El tiempo real en segundos
    """
    def tiempo_real_segundos(self) -> int:
        tiempo = self.tiempo_real(string=False)
        if isinstance(tiempo, timedelta):
            return tiempo.total_seconds()
        else:
            return 0
        
    def diferencia(self) -> str:
        tiempo_estimado = self.tiempo_estimado_segundos()
        tiempo_real = self.tiempo_real_segundos()
        if(tiempo_real == 0):
            return "00:00:00"
        diferencia = tiempo_real - tiempo_estimado
        if diferencia < 0:
            return f'-{str(timedelta(seconds=abs(diferencia)))}'
        else:
            return str(timedelta(seconds=diferencia))

    # def desviacion_tiempo(self) -> float | str:
    #     tiempo = self.tiempo_estimado(string=False)
    #     real = self.tiempo_real(string=False)
    #     if (isinstance(tiempo, timedelta) and isinstance(real, timedelta)):
    #         tiempo = tiempo.total_seconds()
    #         real = real.total_seconds() if real is not None else 0
    #         desviacion = ((real / tiempo) - 1) * 100
    #         return desviacion
    #     else:
    #         return "0"