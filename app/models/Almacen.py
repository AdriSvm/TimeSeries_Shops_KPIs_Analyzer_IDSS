from app import Base
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class Almacen(Base.classes.tbdAlmacenes):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def exists(session: Session, *args) -> list:
        """
        Verifica si uno o más almacenes existen en la base de datos.

        :param session: SQLAlchemy session para realizar la consulta.
        :param args: IDs de almacenes a verificar.
        :return: Lista de booleanos indicando si cada almacén existe.
        """
        return [session.query(Almacen).filter_by(fldIdAlmacen=a).first() is not None for a in args]


