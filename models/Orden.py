from .Model import Model
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .Cliente import Cliente
    from .Producto import Producto
    from .Tamano import Tamano
    from .Color import Color
    from .Incidente import Incidente
    from .BitacoraOrden import BitacoraOrden



class Orden(Model):

    _agregar_atributos = ['tamano', 'cliente_nombre', 'producto_nombre', 'color_nombre']

    __tablename__ = 'ordenes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nro_orden: Mapped[str] = mapped_column(String(50), nullable=False, index=True, comment='Número de orden por parte de la empresa')
    fecha: Mapped[str] = mapped_column(DateTime, nullable=False, comment='Fecha de creacion la orden', default=datetime.now())
    fecha_entrega: Mapped[str] = mapped_column(DateTime, nullable=False, comment='Fecha de entrega de la orden')
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey('clientes.id'), nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, ForeignKey('productos.id'), nullable=False)
    ancho: Mapped[int] = mapped_column(Integer, nullable=True)
    alto: Mapped[int] = mapped_column(Integer, nullable=True)
    largo: Mapped[int] = mapped_column(Integer, nullable=True)
    color_id: Mapped[int] = mapped_column(Integer, ForeignKey('colores.id'), nullable=True)
    observaciones: Mapped[str] = mapped_column(String(250), nullable=True)
    estado: Mapped[str] = mapped_column(String(50), nullable=True, default='creada', comment='Estado de la orden (creada, proceso, finalizada, cancelada, entregada)')

    # Relaciones
    cliente: Mapped['Cliente'] = relationship('Cliente', overlaps='ordenes')
    producto: Mapped['Producto'] = relationship('Producto')
    color: Mapped['Color'] = relationship('Color', backref='ordenes')
    incidentes:Mapped[List['Incidente']] = relationship("Incidente")
    bitacora_ultimo:Mapped['BitacoraOrden'] = relationship(
        "BitacoraOrden", uselist=False, order_by="desc(BitacoraOrden.id)")
    bitacora:Mapped[List['BitacoraOrden']] = relationship("BitacoraOrden", order_by="desc(BitacoraOrden.id)", overlaps='bitacora_ultimo')

    def tamano(self) -> str:
        alto = self.alto if self.alto else 0
        largo = self.largo if self.largo else 0
        ancho = self.ancho if self.ancho else 0
        return f'{alto}x{largo}x{ancho}'

    def cliente_nombre(self) -> str:
        return self.cliente.nombre
    
    def producto_nombre(self) -> str:
        return self.producto.nombre
    
    def color_nombre(self) -> str:
        return self.color.nombre if self.color else 'Sin color'
    
        