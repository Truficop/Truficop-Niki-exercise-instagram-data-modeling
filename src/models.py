import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()



follow = Table(
    'follow',
Base.metadata,
Column('following_id',Integer,ForeignKey('User.id')),
Column('follower_id',Integer,ForeignKey('User.id'))
)

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)

    follower = relationship('Follower', 
                                secondary = follow, 
                                primaryjoin = (follow.c.following_id == id),
                                secondaryjoin = (follow.c.follower_id == id),
                                backref = 'following', lazy=True)
    
    post = relationship('Post', backref='User', lazy=True)
    comment = relationship('Comment', backref='User', lazy=True)

# class Follower(Base):
#     __tablename__ = 'Follower'
#     user_from_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
#     user_to_id = Column(Integer, ForeignKey('User.id'), primary_key=True)

class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))

    media = relationship('Media', backref='Post', lazy=True)
    comment = relationship('Comment', backref='Post', lazy=True)

class Media(Base):
    __tablename__ = 'Media'
    id = Column(Integer, primary_key=True)
    type = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'))

class Comment(Base):
    __tablename__ = 'Comment'
    id = Column(Integer, primary_key=True)  
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('User.id'))
    post_id = Column(Integer, ForeignKey('Post.id'))

    def to_dict(self):
        return {}



# ================================== COPIA PARA EL MODELING DE BLOG DE STAR WARS ===========================================
# ====================================================== INICIO ============================================================

# class Usuario(Base):
#     __tablename__ = 'usuario'
#     id = Column(Integer, primary_key=True)
#     email = Column(String(250),nullable=False, unique=True)
#     password = Column(String(250),nullable=False)
#     nombre = Column(String(250),nullable=False)
#     apellido = Column(String(250),nullable=False)
#     fecha_de_subscripcion = Column(DateTime, nullable=False)
#     favoritos_planetas = relationship('FavoritoPlaneta', backref='usuario')
#     favoritos_personajes = relationship('FavoritoPersonaje', backref='usuario')


# class Planeta(Base):
#     __tablename__ = 'planeta'
#     id = Column(Integer, primary_key=True)
#     nombre = Column(String(250), nullable=False)
#     population = Column(Integer, nullable=False)
#     rotation_period = Column(Integer, nullable=False)
#     orbital_period = Column(Integer, nullable=False)
#     diameter = Column(Integer, nullable=False)
#     gravity = Column(String(250), nullable=False)
#     terrain = Column(String(250), nullable=False)
#     surface = Column(String(250), nullable=False)
#     climate = Column(String(250), nullable=False)
#     favoritos_planetas = relationship('FavoritoPlaneta', backref='planeta')


# class Personaje(Base):
#     __tablename__ = 'personaje'
#     id = Column(Integer, primary_key=True)
#     nombre = Column(String(250), nullable=False)
#     birth_year = Column(Integer, nullable=False)
#     species = Column(String(250), nullable=False)
#     height = Column(Integer, nullable=False)
#     mass = Column(Integer, nullable=False)
#     gender = Column(String(250), nullable=False)
#     hair_color = Column(String(250), nullable=False)
#     skin_color = Column(String(250), nullable=False)
#     homeworld = Column(String(250), ForeignKey('planeta.id'))
#     favoritos_personajes = relationship('FavoritoPersonaje', backref='personaje')


# class FavoritoPlaneta(Base):
#     __tablename__ = 'favorito_planeta'
#     id = Column(Integer, primary_key=True)
#     usuario_id = Column(Integer, ForeignKey('usuario.id'))
#     planeta_id = Column(Integer, ForeignKey('planeta.id'))
#     fecha_de_favorito = Column(DateTime, nullable=False)
#     usuario = relationship('Usuario', backref='favoritos_planetas')
#     planeta = relationship('Planeta', backref='favoritos_planetas')


# class FavoritoPersonaje(Base):
#     __tablename__ = 'favorito_personaje'
#     id = Column(Integer, primary_key=True)
#     usuario_id = Column(Integer, ForeignKey('usuario.id'))
#     personaje_id = Column(Integer, ForeignKey('personaje.id'))
#     fecha_de_favorito = Column(DateTime, nullable=False)
#     usuario = relationship('Usuario', backref='favoritos_personajes')
#     personaje = relationship('Personaje', backref='favoritos_personajes')

# ====================================================== FIN ============================================================
# ================================== COPIA PARA EL MODELING DE BLOG DE STAR WARS ===========================================

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
