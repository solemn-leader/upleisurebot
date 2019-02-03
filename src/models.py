# this file describes basic models for  bot to use
from db import db
from playhouse.postgres_ext import *
import os
from consts import ChatStatuses


class Event(Model):
    owner = DeferredForeignKey(
        'User',
        related_name='events',
        to_field='pk'
        )
    pk = AutoField()
    field_type = int
    city = CharField()  # user must have city set
    age_group = IntegerField()  # user must have age set

    class Meta:
        database = db


class User(Model):
    name = CharField()
    pk = AutoField()

    last_seen_event = ForeignKeyField(
        Event.city,
        to_field='pk'
    )
    seen_events_pks = ArrayField(
        IntegerField
    )

    class Meta:
        database = db


class Metrics(Model):
    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Event, User, Metrics])


if os.environ.get("DEPLOYED_LOCALLY", 0):
    create_tables()
