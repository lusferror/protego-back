from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime

db = SQLAlchemy()

class Model(db.Model):

    _agregar_atributos = []
    _ocultar = []
    __abstract__ = True

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    def serializar(self, ocultar=[], show=[], relaciones=[]):
        data = {}
        ocultar_todo = [*self._ocultar, *ocultar]
        for columna in self.__table__.columns:
            if columna.name in ocultar_todo:
                continue
            if len(show) and columna.name not in show:
                continue
            valor_columna = getattr(self, columna.name)
            if isinstance(valor_columna, datetime):
                data[columna.name] = valor_columna.strftime('%Y-%m-%d %H:%M:%S')
            else:
                data[columna.name] = valor_columna
        for relation in relaciones:
            dividir_relacion: list = relation.split(".")
            secondary_relation = dividir_relacion[1].replace('[', '').replace(']', '') if len(
                dividir_relacion) > 1 else []
            secondary_relation = secondary_relation.split(",") if len(
                secondary_relation) > 0 else []
            if dividir_relacion[0] in self.__class__.__mapper__.relationships.keys() and getattr(self, dividir_relacion[0]) is not None:

                if isinstance(getattr(self, dividir_relacion[0]), list):
                    data[dividir_relacion[0]] = [item.serializar(relaciones=secondary_relation)
                                               for item in getattr(self, dividir_relacion[0])]
                else:
                    data[dividir_relacion[0]] = getattr(
                        self, dividir_relacion[0]).serializar(relaciones=secondary_relation)

        for attribute in self._agregar_atributos:
            data[attribute] = getattr(self, attribute)()
        return data
    
    created_at: Mapped[str] = mapped_column(DateTime, nullable=False, comment='Fecha de creacion del registro', default=datetime.now())
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=False, comment='Fecha de actualizacion del registro', default=datetime.now())
    deleted_at: Mapped[str] = mapped_column(DateTime, nullable=True, comment='Fecha de eliminacion del registro')
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data: dict = {}):
        for key, value in data.items():
            if hasattr(self, key) and value is not None and key != 'id':
                setattr(self, key, value)
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        self.deleted_at = datetime.now()
        db.session.commit()