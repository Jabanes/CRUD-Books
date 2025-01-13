from flask import Blueprint, jsonify, request
from crud import *


manage_loans = Blueprint('manage_loans', __name__)
@manage_loans.route('/loans', methods=['GET', 'POST', 'DELETE'])
def manageLoans():
    if request.method == 'GET':

        filter_type = request.args.get('filter', 'active') 
        
        if filter_type == 'active':
            active_loans = display_loaned_books()
            return jsonify(active_loans)

        if filter_type == 'history':
            loaned_books = display_all_loans()
            return jsonify(loaned_books)

        if  filter_type == 'returned':
            returned_loans = display_returned_loans()
            return jsonify(returned_loans)
        
               

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


