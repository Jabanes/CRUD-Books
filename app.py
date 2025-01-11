from flask import Flask
from crud import home_page, manage_books, manage_customers, manage_loans
from db import init_db


app = Flask(__name__)

init_db()

app.register_blueprint(home_page)
app.register_blueprint(manage_books)
app.register_blueprint(manage_customers)
app.register_blueprint(manage_loans)

if __name__ == "__main__":
    app.run(debug=True)
   