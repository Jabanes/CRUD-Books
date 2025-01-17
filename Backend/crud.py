from flask import request
from models import *
from db import db_session 
from datetime import date, datetime, timedelta
from sqlalchemy import func

#CRUD BOOKS
def add_new_book(bookName, bookAuthor, yearPublished, bookType, bookGenre):
    new_book = Book(name=bookName, author=bookAuthor, yearPublished=yearPublished, type=BookType(bookType), genre=bookGenre)
    db_session.add(new_book)
    db_session.commit()

def find_book_by_name(book_to_find):
    book = db_session.query(Book).filter(func.lower(Book.name) == func.lower(book_to_find)).first()
    
    if book:
        book_data = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "yearPublished": book.yearPublished,
            "type": book.type.value,  
            "available": book.available
        }
        return book_data 
    
 
    return {"message": "Book not found"}


def display_all_books():
    books = db_session.query(Book).all()
    books_list = []
    for book in books:
        book_data = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "yearPublished": book.yearPublished,
            "genre" : book.genre,
            "type": book.type.value,  
            "available": book.available
        }
        books_list.append(book_data)
    return books_list

def display_available_books():
    available_books = db_session.query(Book).filter_by(available = True).all()
    available_books_list = []
    for book in available_books:
        book_data = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "yearPublished": book.yearPublished,
            "genre" : book.genre,
            "type": book.type.value,  
            "available": book.available
        }
        available_books_list.append(book_data)
    return available_books_list

def display_unavailable_books():
    unavailable_books = db_session.query(Book).filter_by(available = False).all()
    unavailable_books_list = []
    for book in unavailable_books:
        book_data = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "yearPublished": book.yearPublished,
            "type": book.type.value,  
            "available": book.available
        }
        unavailable_books_list.append(book_data)
    return unavailable_books_list

def update_book():
    data = request.get_json()
    id_to_update = data.get('id')
    new_bookName = data.get('name')
    new_bookAuthor = data.get('author')
    new_yearPublished = data.get('yearPublished')
    new_genre = data.get('genre')
    new_bookType = data.get('type')

    book = db_session.query(Book).get(id_to_update)

    book.name = new_bookName if new_bookName else book.name
    book.author = new_bookAuthor if new_bookAuthor else book.author
    book.new_yearPublished = new_yearPublished if new_yearPublished else book.yearPublished
    book.genre = new_genre if new_genre else book.genre
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

def find_customer_by_name(customer_to_find):
    customer = db_session.query(Customer).filter(func.lower(Customer.name) == func.lower(customer_to_find)).first()
        
    if customer:
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "city": customer.city,
            "age": customer.age,
            "active": customer.active
        }
        return customer_data  
        
    
    return {"message": "Customer not found"}

def display_all_customers():
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

def display_active_customers():
    active_customers = db_session.query(Customer).filter_by(active=True).all()
    active_customers_list = []
    for customer in active_customers:
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "city" : customer.city,
            "age": customer.age,
            "active": customer.active
        }
        active_customers_list.append(customer_data)
    return active_customers_list

def display_inactive_customers():
    inactive_customers = db_session.query(Customer).filter_by(active=False).all()
    inactive_customers_list = []
    for customer in inactive_customers:
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "city" : customer.city,
            "age": customer.age,
            "active": customer.active
        }
        inactive_customers_list.append(customer_data)
    return inactive_customers_list

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
def loan_book(customer_id, book_id, loan_date):
    
    loan_date = datetime.strptime(loan_date, '%d-%m-%Y',).date()
    
    loaned_book = db_session.query(Book).filter_by(id=book_id).first()

    if loaned_book:

        if loaned_book.type == BookType.type1:
            return_date = loan_date + timedelta(days=10)
        elif loaned_book.type == BookType.type2:
            return_date = loan_date + timedelta(days=5)
        elif loaned_book.type == BookType.type3:
            return_date = loan_date + timedelta(days=2)
        else:
            return {"message": "Invalid book type"}
        
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

#display only loans with is_returned = false
def display_loaned_books():
    active_loans = db_session.query(Loan).filter_by(is_returned=False).all()
    active_loans_list = []

    for loan in active_loans:
        loaned_books_data = {
            "loan_id": loan.loan_id, 
            "customer_id": loan.customer_id,
            "book_id" : loan.book_id,
            "loan_date": loan.loan_date,
            "return_date": loan.return_date,
            "is_returned" : loan.is_returned
        }
        active_loans_list.append(loaned_books_data)
    return active_loans_list
#return a book - change availablity form fale to true, 

def display_returned_loans():
    returned_loans = db_session.query(Loan).filter_by(is_returned=True).all()
    returned_loans_list = []

    for loan in returned_loans:
        loaned_books_data = {
            "loan_id": loan.loan_id, 
            "customer_id": loan.customer_id,
            "book_id" : loan.book_id,
            "loan_date": loan.loan_date,
            "return_date": loan.return_date,
            "is_returned" : loan.is_returned
        }
        returned_loans_list.append(loaned_books_data)
    return returned_loans_list

    
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
    
    current_date = date.today()
    late_loans = db_session.query(Loan).filter(Loan.is_returned == False).all()

    late_loans_list = []

    
    for loan in late_loans:
        if loan.return_date < current_date:
            loan_data = {
                "loan_id": loan.loan_id,
                "customer_id": loan.customer_id,
                "book_id": loan.book_id,
                "loan_date": loan.loan_date,
                "return_date": loan.return_date,
                "is_returned": loan.is_returned
            }
            late_loans_list.append(loan_data)

    return late_loans_list

