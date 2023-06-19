from peewee import IntegerField, CharField, Model, UUIDField

from src.db import db


class User(Model):
    # primary guid
    id = CharField(unique=True, primary_key=True)

    class Meta:
        database = db
