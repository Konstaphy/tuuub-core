from flask import Flask

from flask_cors import CORS
from dotenv import load_dotenv

from src.db import db
from src.modules.reactions.controller.reaction_controller import reaction_controller
from src.modules.reactions.model.reaction_model import Reaction
from src.modules.users.model.user_model import User
from src.modules.users.controller.users_controller import users_controller
from src.modules.videos.model.video_model import Video
from src.modules.videos.controller.videos_controller import video_controller


def create_app():
    # set environment variables from .env
    load_dotenv()

    flask_app = Flask(__name__)
    db.connect()
    User.create_table()
    Video.create_table()
    Reaction.create_table()
    # initializing app
    CORS(flask_app, supports_credentials=True)
    # register blueprints
    flask_app.register_blueprint(users_controller)
    flask_app.register_blueprint(reaction_controller)
    flask_app.register_blueprint(video_controller)

    return flask_app


if __name__ == "__main__":
    app = create_app()
    # run app in 8080
    app.run(port=8080)
