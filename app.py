import sys
from flask import Flask, request
from loguru import logger
from flask_cors import CORS
from blueprints.home_bp import home_page
from blueprints.books_bp import manage_books
from blueprints.customers_bp import manage_customers
from blueprints.loans_bp import manage_loans
from db import init_db

app = Flask(__name__)
CORS(app)
init_db()

logger.remove()
logger.add(sys.stdout, level="DEBUG", format="{time} {level} {message}")
logger.add("../../../Logs/library.log", rotation="1 day", retention="7 days", level="DEBUG", format="{time} {level} {message}")

@app.before_request
def log_request_info():
    logger.info(f"Request: method={request.method}, path={request.path}, args={request.args}, from IP={request.remote_addr}")



app.register_blueprint(home_page)
app.register_blueprint(manage_books)
app.register_blueprint(manage_customers)
app.register_blueprint(manage_loans)

if __name__ == "__main__":
    app.run(debug=True)
   