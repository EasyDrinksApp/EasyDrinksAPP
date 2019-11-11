from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Clientes(db.Model):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    usuario = Column(String(50))
    password_hash = Column(String(128), nullable=False)
    nombre = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Productos(db.Model):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    precio = Column(Float, default=0)
    stock = Column(Integer)
    categoriaId = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    categoria = relationship("Categorias", backref="Productos")

    def precio_final(self):
        return self.precio

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Categorias(db.Model):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(15))
    productos = relationship("Productos", cascade="all, delete-orphan", backref="Categorias")
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
