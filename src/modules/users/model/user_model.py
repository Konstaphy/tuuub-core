from peewee import IntegerField, CharField, Model, UUIDField

from src.database.db import db


class User(Model):
    # primary guid
    id = UUIDField(unique=True, primary_key=True)
    # default login identification
    username = CharField(unique=True)
    # for password reset and 2-factor auth
    email = CharField(unique=True)
    # encrypted
    password = CharField()
    # for age restrictions
    age = IntegerField()

    class Meta:
        database = db
