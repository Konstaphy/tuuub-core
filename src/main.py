from flask import Flask

from src.views.users.users import users_view
from src.database.db import db
from flask_cors import CORS

from src.views.video.video import video_view

if __name__ == "__main__":
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.register_blueprint(users_view, url_prefix="/users")
    app.register_blueprint(video_view, url_prefix="/videos")
    # initializing db cursor
    db = db.cursor()
    # run app in 8080
    app.run(port=8080)
