from flask import Flask
from src.database.db import db
from flask_cors import CORS

if __name__ == "__main__":
    app = Flask(__name__)
    # initializing db cursor
    db = db.cursor()
    CORS(app, supports_credentials=True)
    # run app in 8080
    app.run(port=8080)
