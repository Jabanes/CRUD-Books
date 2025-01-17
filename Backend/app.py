import sys
from flask import Flask, request
from loguru import logger
from flask_cors import CORS
from blueprints.index_bp import index_page
from blueprints.books_bp import manage_books
from blueprints.customers_bp import manage_customers
from blueprints.home_bp import home_page
from blueprints.loans_bp import manage_loans
from db import init_db

app = Flask(__name__, static_folder='../Frontend/static')
CORS(app)
CORS(app, resources={r"/*": {
    "origins": "http://127.0.0.1:5500",  # Use the exact origin where you're running your frontend
    "methods": ["POST", "GET", "PUT", "DELETE"],
    "allow_headers": ["Content-Type"]
}})

init_db()

logger.remove()
logger.add(sys.stdout, level="DEBUG", format="{time} {level} {message}")
logger.add("../../../Logs/library.log", rotation="1 day", retention="7 days", level="DEBUG", format="{time} {level} {message}")

@app.before_request
def log_request_info():
    logger.info(f"Request: method={request.method}, path={request.path}, args={request.args}, from IP={request.remote_addr}")


app.register_blueprint(index_page)
app.register_blueprint(home_page)
app.register_blueprint(manage_books)
app.register_blueprint(manage_customers)
app.register_blueprint(manage_loans)

if __name__ == "__main__":
    app.run(debug=True)
   