# this file describes basic models for  bot to use
from db import db
from peewee import *
import os
from consts import ChatStatuses


class User(Model):
    name = CharField()
    pk = IntegerField()  # user's vk id
    chat_status = IntegerField()

    class Meta:
        database = db


class Event(Model):
    owner = ForeignKeyField(
        User,
        related_name='events'
        )
    
    city = CharField()  # user must have city set

    age_group = IntegerField()  # user must have age set

    class Meta:
        database = db


class Metrics(Model):
    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([User, Event, Metrics])


if os.environ.get("DEPLOYED_LOCALLY", 0):
    create_tables()
