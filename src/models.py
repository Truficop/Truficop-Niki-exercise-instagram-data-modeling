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

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
