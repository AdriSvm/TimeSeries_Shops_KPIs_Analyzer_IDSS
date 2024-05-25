from sqlalchemy.inspection import inspect
from app import Base



class User(Base.classes.tbdAccesosUsuario):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self) -> dict:
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def is_admin(self):
        return self.fldIdNivelAcceso == '1111'

