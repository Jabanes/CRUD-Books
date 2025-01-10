from sqlalchemy import Column, Integer, String, Enum, Boolean
from db import Base
from enum import Enum as PyEnum

class BookType(PyEnum):
    type1 = 1 
    type2 = 2 
    type3 = 3 

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    author = Column(String(120), unique=False)
    yearPublished = Column(Integer, unique=False)
    type = Column(Enum(BookType), nullable=False)
    available = Column(Boolean, default=True)

def __repr__(self):
    return f'<Book {self.name!r},Author {self.author!r}, ({self.yearPublshed!r}) >'
        
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    city = Column(String(120), unique=False)
    age = Column(Integer, unique=False)
    active = Column(Boolean, default=True) 

def __repr__(self):
    return f'<Name {self.name!r},City {self.city!r}, Age {self.age!r} >'