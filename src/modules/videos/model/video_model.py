from peewee import Model, CharField, ForeignKeyField, UUIDField

from src.db import db
from src.modules.users.model.user_model import User


class Video(Model):

    id = UUIDField(unique=True, primary_key=True)
    title = CharField()
    description = CharField()
    file_path = CharField()
    user_id = ForeignKeyField(User, backref='videos')

    class Meta:
        database = db
