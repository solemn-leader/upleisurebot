import os

from playhouse.db_url import connect
from playhouse.postgres_ext import PostgresqlExtDatabase

if os.environ.get("DEPLOYED_LOCALLY", False):
    db = PostgresqlExtDatabase(
        'postgres',
        user='postgres',
        host='bot_db',
        port=5432,
        sslmode='disable'
    )
else:
    db = connect(
        (os.environ.get('DATABASE_URL'))
    )
