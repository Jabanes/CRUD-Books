from sqlalchemy import Column, Integer, String, Enum, Boolean, Date
from sqlalchemy.orm import relationship
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
    loans = relationship("Loan", back_populates="book")

def __repr__(self):
    return f'<Book {self.name!r},Author {self.author!r}, ({self.yearPublshed!r}) >'
        
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    city = Column(String(120), unique=False)
    age = Column(Integer, unique=False)
    active = Column(Boolean, default=True) 
    loans = relationship("Loan", back_populates="customer")

def __repr__(self):
    return f'<Name {self.name!r},City {self.city!r}, Age {self.age!r} >'

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, unique=False)
    book_id = Column(Integer, unique=False)
    loan_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    is_returned =  Column(Boolean, default=False)
    customer = relationship("Customer", back_populates="loans")
    book = relationship("Book", back_populates="loans")

