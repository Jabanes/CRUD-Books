from flask import jsonify, request
from models import *
from db import db_session 
from datetime import date, datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import joinedload

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

def find_book_by_id(id_to_find):
    book = db_session.query(Book).filter(Book.id == id_to_find).first()  

    if book:
        book_data = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "yearPublished": book.yearPublished,
            "type": book.type.value, 
            "genre": book.genre,
            "available": book.available
        }
        return book_data 
    
 
    return {"message": "Book not found"}


def display_all_books():
    books = db_session.query(Book).all()
    return [
        {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "yearPublished": book.yearPublished,
            "genre": book.genre,
            "type": book.type.value,
            "available": book.available
        }
        for book in books
    ]

def display_available_books():
    books = db_session.query(Book).filter_by(available=True).all()
    return [
        {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "yearPublished": book.yearPublished,
            "genre": book.genre,
            "type": book.type.value,
            "available": book.available
        }
        for book in books
    ]

def display_unavailable_books():
    unavailable_books = db_session.query(Book).filter_by(available = False).all()
    return [
        {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "yearPublished": book.yearPublished,
            "genre": book.genre,
            "type": book.type.value,
            "available": book.available
        }
        for book in unavailable_books
    ]

def update_book():
    data = request.get_json()
    id_to_update = data.get('id')
    new_bookName = data.get('name')
    new_bookAuthor = data.get('author')
    new_yearPublished = data.get('yearPublished')
    new_genre = data.get('genre')
    new_bookType = data.get('type')

    # Fetch the book from the database
    book = db_session.query(Book).get(id_to_update)
    
    # Check if the book exists
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    # Update fields if new data is provided
    book.name = new_bookName if new_bookName else book.name
    book.author = new_bookAuthor if new_bookAuthor else book.author
    book.yearPublished = new_yearPublished if new_yearPublished else book.yearPublished
    book.genre = new_genre if new_genre else book.genre
    book.type = BookType(new_bookType) if new_bookType else book.type
   
    try:
        db_session.commit()
        return jsonify({'success': True, 'message': 'Book updated successfully'}), 200
    except Exception as e:
        db_session.rollback()  # Rollback on error
        print(f"Error committing changes: {e}")
        jsonify({'error': 'An error occurred while updating the book'}), 500

    # Return success message
    return jsonify({'success': True, 'message': 'Book updated successfully'}), 200
    
def delete_book():
    data = request.get_json()
    id_to_delete = data.get('id')
    book = db_session.query(Book).get(id_to_delete)
    
    book.available = False
    db_session.commit()

def restore_book():
    data = request.get_json()
    id_to_delete = data.get('id')
    book = db_session.query(Book).get(id_to_delete)
    
    book.available = True
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

def find_customer_by_id(id_to_find):
    customer = db_session.query(Customer).filter(Customer.id == id_to_find).first()  

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
    return [
        {
            "id": customer.id,
            "name": customer.name,
            "city": customer.city,
            "age": customer.age,
            "active": customer.active
        }
        for customer in customers
    ]

def display_active_customers():
    active_customers = db_session.query(Customer).filter_by(active=True).all()
    return [
        {
            "id": customer.id,
            "name": customer.name,
            "city": customer.city,
            "age": customer.age,
            "active": customer.active
        }
        for customer in active_customers
    ]

def display_inactive_customers():
    inactive_customers = db_session.query(Customer).filter_by(active=False).all()
    return [
        {
            "id": customer.id,
            "name": customer.name,
            "city": customer.city,
            "age": customer.age,
            "active": customer.active
        }
        for customer in inactive_customers
    ]

def update_customer():
    data = request.get_json()
    id_to_update = data.get('id')
    new_customer_name = data.get('name')
    new_customer_city = data.get('city')
    new_customer_age = data.get('age')
    

    customer = db_session.query(Customer).get(id_to_update)

    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    customer.name = new_customer_name if new_customer_name else customer.name
    customer.city = new_customer_city if new_customer_city else customer.city
    customer.age = new_customer_age if new_customer_age else customer.age

    try:
        db_session.commit()
        return jsonify({'success': True, 'message': 'Customer updated successfully'}), 200
    except Exception as e:
        db_session.rollback()  # Rollback on error
        print(f"Error committing changes: {e}")
        jsonify({'error': 'An error occurred while updating the Customer'}), 500

    # Return success message
    return jsonify({'success': True, 'message': 'Customer updated successfully'}), 200

def delete_customer():
    data = request.get_json()
    id_to_delete = data.get('id')
    customer = db_session.query(Customer).get(id_to_delete)
    
    customer.active = False
    db_session.commit()

def restore_customer():
    data = request.get_json()
    id_to_delete = data.get('id')
    customer = db_session.query(Customer).get(id_to_delete)
    
    customer.active = True
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
        db_session.add(new_loan)
        db_session.commit()

    else:
        print("Book was not found")

#display all loans ever made
def display_all_loans():
    loaned_books = db_session.query(Loan).options(
        joinedload(Loan.customer),
        joinedload(Loan.book)
    ).all()

    # Use a list comprehension to process the data
    return [
        {
            "loan_id": loan.loan_id,
            "customer": loan.customer.name if loan.customer else "Unknown",
            "book": loan.book.name if loan.book else "Unknown",
            "loan_date": loan.loan_date.strftime('%a, %d %b %Y') if loan.loan_date else "Unknown",
            "return_date": loan.return_date.strftime('%a, %d %b %Y') if loan.return_date else "Unknown",
            "is_returned": loan.is_returned
        }
        for loan in loaned_books
    ]

#display only loans with is_returned = false
def display_loaned_books():
    active_loans = db_session.query(Loan).filter_by(is_returned=False).options(
        joinedload(Loan.customer),
        joinedload(Loan.book)
    ).all()

    # Use a list comprehension to process the data
    return [
        {
            "loan_id": loan.loan_id,
            "customer": loan.customer.name if loan.customer else "Unknown",
            "book_id": loan.book.name if loan.book else "Unknown",
            "loan_date": loan.loan_date.strftime('%a, %d %b %Y') if loan.loan_date else "Unknown",
            "return_date": loan.return_date.strftime('%a, %d %b %Y') if loan.return_date else "Unknown",
            "is_returned": loan.is_returned
        }
        for loan in active_loans
    ]
#return a book - change availablity form fale to true, 

def display_returned_loans():
    active_loans = db_session.query(Loan).filter_by(is_returned=True).options(
        joinedload(Loan.customer),
        joinedload(Loan.book)
    ).all()

    # Use a list comprehension to process the data
    return [
        {
            "loan_id": loan.loan_id,
            "customer": loan.customer.name if loan.customer else "Unknown",
            "book_id": loan.book.name if loan.book else "Unknown",
            "loan_date": loan.loan_date.strftime('%a, %d %b %Y') if loan.loan_date else "Unknown",
            "return_date": loan.return_date.strftime('%a, %d %b %Y') if loan.return_date else "Unknown",
            "is_returned": loan.is_returned
        }
        for loan in active_loans
    ]
    
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

    # Fetch all loans that are not returned with related customer and book data using joinedload
    late_loans = db_session.query(Loan).filter(Loan.is_returned == False).options(
        joinedload(Loan.customer),
        joinedload(Loan.book)
    ).all()

    # Use list comprehension to filter and process the data
    return [
        {
            "loan_id": loan.loan_id,
            "customer": loan.customer.name if loan.customer else "Unknown",
            "book": loan.book.name if loan.book else "Unknown",
            "loan_date": loan.loan_date.strftime('%a, %d %b %Y') if loan.loan_date else "Unknown",
            "return_date": loan.return_date.strftime('%a, %d %b %Y') if loan.return_date else "Unknown",
            "is_returned": loan.is_returned
        }
        for loan in late_loans
        if loan.return_date and loan.return_date < current_date
    ]

