from sqlalchemy.orm import relationship

from app import Base
from sqlalchemy.inspection import inspect

class Cliente(Base.classes.tbdAttClientes):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    tiquets = relationship('TiquetCabecera', back_populates="cliente",
                           primaryjoin="foreign(TiquetCabecera.fldIdCliente) == remote(Cliente.fldIdCliente)",
                           lazy=True)

    def to_dict(self) -> dict:
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}