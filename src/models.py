# this file describes basic models for  bot to use
from db import db
from peewee import *


class User(Model):
    name = CharField()
    pk = CharField()  # user's id

    class Meta:
        database = db


class Event(Model):
    owner = ForeignKeyField(
        User,
        related_name='events'
        )

    class Meta:
        database = db


class Metrics(Model):
    class Meta:
        database = db
