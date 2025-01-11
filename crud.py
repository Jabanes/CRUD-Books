from flask import Blueprint, jsonify, request
from models import *
from db import db_session 
from datetime import datetime

home_page = Blueprint('home_page', __name__)
manage_books = Blueprint('manage_books', __name__)
manage_customers = Blueprint('manage_customers', __name__)
manage_loans = Blueprint('manage_loans', __name__)


#CRUD BOOKS
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
    
    book.available = False
    db_session.commit()
#-------------------------------------

#CRUD CUSTOMERS
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

def update_customer():
    data = request.get_json()
    id_to_update = data.get('id')
    new_customer_name = data.get('name')
    new_customer_city = data.get('city')
    new_customer_age = data.get('age')
    

    customer = db_session.query(Customer).get(id_to_update)

    customer.name = new_customer_name if new_customer_name else customer.name
    customer.city = new_customer_city if new_customer_city else customer.author
    customer.age = new_customer_age if new_customer_age else customer.yearPublished

    db_session.commit()

def delete_customer():
    data = request.get_json()
    id_to_delete = data.get('id')
    customer = db_session.query(Customer).get(id_to_delete)
    
    customer.active = False
    db_session.commit()
#---------------------------------------

#CRUD LOANS
#loan a book - dynamic return date based on book type. change availablity to False
def loan_book(customer_id, book_id, loan_date, return_date):
    
    loan_date = datetime.strptime(loan_date, '%d-%m-%Y',).date()
    return_date = datetime.strptime(return_date, '%d-%m-%Y').date()

    
    loaned_book = db_session.query(Book).filter_by(id=book_id).first()

    if loaned_book:
        loaned_book.available = False

        new_loan = Loan(customer_id=customer_id, book_id=book_id, loan_date=loan_date, return_date=return_date)
        db_session.add(loaned_book)
        db_session.add(new_loan)
        db_session.commit()

    else:
        print("Book was not found")

#display all loans ever made
def display_all_loans():
    loaned_books = db_session.query(Loan).all()
    loaned_books_list = []

    for loan in loaned_books:
        loaned_books_data = {
            "loan_id": loan.loan_id, 
            "customer_id": loan.customer_id,
            "book_id" : loan.book_id,
            "loan_date": loan.loan_date,
            "return_date": loan.return_date,
            "is_returned" : loan.is_returned
        }
        loaned_books_list.append(loaned_books_data)
    return loaned_books_list


#display available books - #display only loans with is_returned = True
def display_available_books():
    pass

#display only loans with is_returned = false
def display_loaned_books():
    pass
#return a book - change availablity form fale to true, 

def return_book():
    data = request.get_json()
    loan_id_to_return = data.get('loan_id')
    loan = db_session.query(Loan).get(loan_id_to_return)

    book_to_return = db_session.query(Book).get(loan.book_id)
    book_to_return.available = True

    loan.is_returned = True
    db_session.commit()

#display all late loans - display all the loans that have surpassed their maximum days to loan 
def display_late_loans():
    pass





@home_page.route('/')
def homePage():
    return 'HOME PAGE'

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
        update_customer()
        return jsonify({"message": "Customer was updated successfully!"}), 200
    
    if request.method== 'DELETE':
        delete_customer()
        return jsonify({"message": "Customer's Status changed to innactive"}), 200

@manage_loans.route('/loans', methods=['GET', 'POST', 'DELETE'])
def manageLoans():
    if request.method == 'GET':
        #display all loans
        loaned_books = display_all_loans()
        return jsonify(loaned_books)

    if request.method == 'POST':
        #loan a book
        data = request.get_json()
        customer_id = data.get('customer_id')
        book_id = data.get('book_id')
        loan_date = data.get('loan_date')
        return_date = data.get('return_date')

        print(f'loaned: {customer_id, book_id, loan_date, return_date}')
        loan_book(customer_id, book_id, loan_date, return_date)

        return jsonify({"message": "New loan was added"}), 201

    if request.method == 'DELETE':
        return_book()
        return jsonify({"message": "Loan was returned successfully!"}, 201)
       