from flask import Blueprint, jsonify, request
from models import *
from db import db_session 

manage_books = Blueprint('manage_books', __name__)
manage_customers = Blueprint('manage_customers', __name__)

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

def add_new_customer(customer_name, customer_city, customer_age):
    new_customer = Customer(name=customer_name, city=customer_city, age=customer_age)
    db_session.add(new_customer)
    db_session.commit()

def display_customers():
    customers = db_session.query(Customer).all()
    customers_list = []
    for customer in customers:
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "city" : customer.city,
            "age": customer.age,
            "active": customer.active
        }
        customers_list.append(customer_data)
    return customers_list

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

@manage_customers.route('/customers', methods=['GET','POST','DELETE','PUT'])
def manageCustomers():
    if request.method == 'GET':
        customers = display_customers()
        return jsonify(customers)
    
    if request.method == 'POST':
        data = request.get_json()
        customerName = data.get('name')
        customerCity = data.get('city')
        customerAge = data.get('age')

        add_new_customer(customerName, customerCity, customerAge)
        return jsonify({"message": "New Customer was added"}), 201
    
    if request.method == 'PUT':

        update_book()
        return jsonify({"message": "Book updated successfully!"}), 200
    
    if request.method== 'DELETE':
        delete_book()
        return jsonify({"message": "Book Changed to unavailable (deleted)"}), 200
    