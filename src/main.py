from flask import Flask

from src.views.users.users import user_bp
from src.database.db import db
from flask_cors import CORS

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(user_bp, url_prefix="/users")
    # initializing db cursor
    db = db.cursor()
    CORS(app, supports_credentials=True)
    # run app in 8080
    app.run(port=8080)
