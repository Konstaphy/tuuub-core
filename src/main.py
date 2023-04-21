from flask import Flask

from flask_cors import CORS
from dotenv import load_dotenv

from src.db import db
from src.modules.users.model.user_model import User
from src.modules.users.controller.users_controller import users_view
from src.modules.videos.model.video_model import Video
from src.modules.videos.controller.videos_controller import video_view

# set environment variables from .env
load_dotenv()

app = Flask(__name__)

if __name__ == "__main__":
    db.connect()
    User.create_table()
    Video.create_table()
    # initializing app
    CORS(app, supports_credentials=True)
    # register blueprints
    app.register_blueprint(users_view)
    app.register_blueprint(video_view)
    # run app in 8080
    app.run(port=8080)
