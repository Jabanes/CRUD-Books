from flask import Flask
from crud import manage_books, manage_customers
from db import init_db


app = Flask(__name__)

init_db()

app.register_blueprint(manage_books)
app.register_blueprint(manage_customers)

@app.route('/')
def home():
    return 'HOME PAGE'

if __name__ == "__main__":
    app.run(debug=True)
   