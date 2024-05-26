from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session

from app import Base



class User(Base.classes.tbdAccesosUsuario):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self) -> dict:
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    @staticmethod
    def exists(session: Session,fldIdGestion:str='PDAS', *args) -> list:
        """
        Verifica si uno o más usuarios existen en la base de datos.

        :param session: SQLAlchemy session para realizar la consulta.
        :param fldIdGestion: ID de gestion del usuario
        :param args: IDs de usuarios a verificar
        :return: Lista de booleanos indicando si cada usuario existe.
        """
        return [session.query(User).filter_by(fldIdGestion=fldIdGestion,fldIdUsuario=a).first() is not None for a in args]

    def is_valid(self):
        if len(self.fldIdUsuario) > 6:
            return False
        if len(self.fldIdClaveAcceso) > 30:
            return False
        if self.fldIdNivelAcceso not in ('0000','1111'):
            return False
        if len(self.fldIdAlmacen) > 8:
            return False
        if len(self.fldIdGestion) > 15:
            return False
        return True



    def is_admin(self):
        return self.fldIdNivelAcceso == '1111'

