from flask import Flask
from crud import manage_books
from db import init_db


app = Flask(__name__)

init_db()

app.register_blueprint(manage_books)


if __name__ == "__main__":
    app.run(debug=True)
    