from flask import Blueprint, jsonify, request
from crud import *

manage_books = Blueprint('manage_books', __name__)

@manage_books.route('/books',methods=['GET','POST','DELETE','PUT'])
def manageBooks():
    if request.method == 'GET':

        book_name = request.args.get('book_name')

        if book_name:
            book = find_book_by_name(book_name)
            if book:  
                return jsonify(book) 
            else:
                return jsonify({"message": "Book not found"}), 404

        
        filter_type = request.args.get('filter', 'available')

        if filter_type == 'available':
            available_books = display_available_books()
            return jsonify(available_books)
        
        if filter_type == 'unavailable':
            unavalabile_books = display_unavailable_books()
            return jsonify(unavalabile_books)
        
        if filter_type == 'all':
            books = display_all_books()
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

  