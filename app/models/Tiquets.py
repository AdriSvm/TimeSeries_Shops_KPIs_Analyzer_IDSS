from sqlalchemy.orm import relationship

from app import Base
from sqlalchemy.inspection import inspect


class TiquetCabecera(Base.classes.tbdTicketCabecera):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    lineas = relationship('TiquetLinea', back_populates="cabecera",
                          primaryjoin="TiquetCabecera.fldIdTicket == TiquetLinea.fldIdTicket",
                          foreign_keys='[TiquetLinea.fldIdTicket]', lazy=True)

    cliente = relationship('Cliente', back_populates="tiquets",
                           primaryjoin="foreign(TiquetCabecera.fldIdCliente) == remote(Cliente.fldIdCliente)",
                           lazy=True)

    def to_dict(self) -> dict:
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class TiquetLinea(Base.classes.tbdTicketLineas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    cabecera = relationship('TiquetCabecera', back_populates="lineas",
                            primaryjoin="TiquetCabecera.fldIdTicket == TiquetLinea.fldIdTicket",
                            foreign_keys='[TiquetLinea.fldIdTicket]', lazy=True)

    def to_dict(self) -> dict:
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}