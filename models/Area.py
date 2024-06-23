from .Model import Model
from sqlalchemy import Integer, String, Boolean, Update
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING
from .Model import db

if TYPE_CHECKING:
    from .Usuario import Usuario

class Area(Model):

    __tablename__ = 'areas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=True)
    finaliza: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

    # Relaciones
    usuarios: Mapped[List['Usuario']] = relationship('Usuario', overlaps='area')

    def _finalizada(self):
        db.session.execute(Update(self.__class__).values(finaliza=not self.finaliza).where(self.__class__.id != self.id))
        self.update()