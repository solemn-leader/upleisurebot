import os
from playhouse.postgres_ext import PostgresqlExtDatabase
from playhouse.db_url import connect

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
