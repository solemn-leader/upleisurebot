# this file describes basic models for  bot to use
from db import db
from playhouse.postgres_ext import *
import os
from consts import (
    ChatStatuses,
    EVENT_DESCRIPTION_MAX_LENGTH, 
    EVENT_ATTACHMENTS_MAX_LENGTH,
    AgeGroups
)
from datetime import datetime


class Event(Model):
    '''basic user uploaded event'''
    '''this model specifies fields but table is not created'''
    owner = DeferredForeignKey(
        'User',
        related_name='events',
        to_field='pk'
        )  # user who uploads event
    pk = BigAutoField(
        primary_key=True
    )
    time_published = DateTimeField(
        default=datetime.utcnow
    )  # when user has uploaded the event

    city = CharField()  # city where owner lives

    description = CharField(
        max_length=EVENT_DESCRIPTION_MAX_LENGTH
    )  # event description

    attachments = CharField(
        max_length=EVENT_ATTACHMENTS_MAX_LENGTH
    )  # event attachments (pics, videos etc.)

    class Meta:
        database = db


class TeenEvent(Event):
    '''event model for users who belong to teen age group'''
    age_group = IntegerField(
        default=AgeGroups.TEENS
    )  # user must have age set


class YoungEvent(Event):
    '''event model for users who belong to young age group'''
    age_group = IntegerField(
        default=AgeGroups.YOUNG
    )  # user must have age set


class User(Model):
    '''basic model representing user bot interacts with'''
    name = CharField()  # user full name

    pk = BigAutoField(
        primary_key=True
    )
    user_id = IntegerField( 
        unique=True
    )  # user vk id
    city = CharField()  # city user lives in

    age_group = IntegerField()  # either teen or young age_group

    last_seen_event_pk = IntegerField(
        default=0
    )  # obvious

    chat_status = IntegerField(

    )  # user chat status

    class Meta:
        database = db


class Metrics(Model):
    class Meta:
        database = db


def create_tables():
    db.create_tables([TeenEvent, YoungEvent, User, Metrics])
