from peewee import Model, ForeignKeyField

from src.db import db
from src.modules.users.model.user_model import User
from src.modules.videos.model.video_model import Video


class Reaction(Model):
    user_id = ForeignKeyField(User, backref='reactions')
    video_id = ForeignKeyField(Video, backref='reactions')

    class Meta:
        database = db

