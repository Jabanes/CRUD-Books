import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///C:/Users/erezh/JohnBryceProjects/Projects/PYTHON/CRUD-Library/Backend/library.db')
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=True,bind=engine))
Base = declarative_base()


conn = sqlite3.connect('library.db',check_same_thread=False)
cursor = conn.cursor()

def init_db():
    Base.metadata.create_all(engine)
