from flask import Flask
from flask_cors import CORS
from blueprints.home_bp import home_page
from blueprints.books_bp import manage_books
from blueprints.customers_bp import manage_customers
from blueprints.loans_bp import manage_loans
from db import init_db


app = Flask(__name__)
CORS(app)

init_db()

app.register_blueprint(home_page)
app.register_blueprint(manage_books)
app.register_blueprint(manage_customers)
app.register_blueprint(manage_loans)

if __name__ == "__main__":
    app.run(debug=True)
   