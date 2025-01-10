from flask import Blueprint, jsonify, request
from models import *
from db import db_session 

manage_books = Blueprint('manage_books', __name__)

def add_new_book(bookName, bookAuthor, yearPublished, bookType):
    new_book = Book(name=bookName, author=bookAuthor, yearPublished=yearPublished, type=BookType(bookType))
    db_session.add(new_book)
    db_session.commit()

def display_books():
    books = db_session.query(Book).all()
    books_list = []
    for book in books:
        book_data = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "yearPublished": book.yearPublished,
            "type": book.type.value,  
            "available": book.available
        }
        books_list.append(book_data)
    return books_list

def update_book():
    data = request.get_json()
    id_to_update = data.get('id')
    new_bookName = data.get('name')
    new_bookAuthor = data.get('author')
    new_yearPublished = data.get('yearPublished')
    new_bookType = data.get('type')

    book = db_session.query(Book).get(id_to_update)

    book.name = new_bookName if new_bookName else book.name
    book.author = new_bookAuthor if new_bookAuthor else book.author
    book.new_yearPublished = new_yearPublished if new_yearPublished else book.yearPublished
    book.type = BookType(new_bookType) if new_bookType else book.type

    db_session.commit()
    
def delete_book():
    data = request.get_json()
    id_to_delete = data.get('id')
    book = db_session.query(Book).get(id_to_delete)
    
    print(book)
    book.available = False
    db_session.commit()

@manage_books.route('/books',methods=['GET','POST','DELETE','PUT'])
def manageBooks():
    if request.method == 'GET':
        books = display_books()
        return jsonify(books)
    
    if request.method == 'POST':
        data = request.get_json()
        bookName = data.get('name')
        bookAuthor = data.get('author')
        yearPublished = data.get('yearPublished')
        bookType = data.get('type')

        add_new_book(bookName, bookAuthor, yearPublished, bookType)

        return jsonify({"message": "New book added"}), 201
    
    if request.method == 'PUT':

        update_book()
        return jsonify({"message": "Book updated successfully!"}), 200
    
    if request.method== 'DELETE':
        delete_book()
        return jsonify({"message": "Book Changed to unavailable (deleted)"}), 200