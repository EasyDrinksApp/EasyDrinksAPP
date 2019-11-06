from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from App import db

class Clientes(db.Model):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    usuario = Column(String(50))
    password = Column(String(8))

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Productos(db.Model):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    precio = Column(String(10))
    stock = Column(String(5))

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

