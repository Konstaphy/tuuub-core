from flask import Flask

from src.database.db import db
from flask_cors import CORS
from dotenv import load_dotenv

from src.modules.users.view.users_view import users_view
from src.modules.videos.view.videos_view import video_view

# set environment variables from .env
load_dotenv()


if __name__ == "__main__":
    # initializing db cursor
    db = db.cursor()
    # initializing app
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # register blueprints
    app.register_blueprint(users_view, url_prefix="/users")
    app.register_blueprint(video_view, url_prefix="/videos")
    # run app in 8080
    app.run(port=8080)
