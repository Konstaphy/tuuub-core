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

# set environment variables from .env
load_dotenv()

app = Flask(__name__)

if __name__ == "__main__":
    db.connect()
    User.create_table()
    Video.create_table()
    Reaction.create_table()
    # initializing app
    CORS(app, supports_credentials=True)
    # register blueprints
    app.register_blueprint(users_controller)
    app.register_blueprint(reaction_controller)
    app.register_blueprint(video_controller)
    # run app in 8080
    app.run(port=8080)
