from .Model import Model
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .Producto import Producto

class Tamano(Model):

    __tablename__ = 'tamanos'

    _agregar_atributos = ['nombre_tamano']

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    producto_id: Mapped[int] = mapped_column(Integer,ForeignKey('productos.id'), nullable=False )
    largo: Mapped[int] = mapped_column(Integer, nullable=False)
    ancho: Mapped[int] = mapped_column(Integer, nullable=False)
    alto: Mapped[int] = mapped_column(Integer, nullable=False)

    #Relaciones
    producto: Mapped['Producto'] = relationship("Producto", back_populates='tamanos')

    def nombre_tamano(self) -> str:
        return f"{self.largo}x{self.ancho}x{self.alto}"