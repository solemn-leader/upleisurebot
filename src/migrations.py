'''this file is responsible for
altering db tables'''
from playhouse.migrate import *
from db import db

migrator = PostgresqlMigrator(db)
'''
how to run migrations:

migrate(
    migrator.add_column('event', 'title', CharField(default='')),
    migrator.rename_column('user', 'name', 'username'),
    migrator.drop_column('metrics', 'n_seen'),
)
'''
