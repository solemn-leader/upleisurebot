import os
from playhouse.postgres_ext import PostgresqlExtDatabase
from playhouse.db_url import connect

if os.environ.get("DEPLOYED_LOCALLY", False):
    db = PostgresqlExtDatabase(
        'postgres',
        user='postgres',
        host='db',
        port=5432,
    )
else:
    db = connect(
        connect(os.environ.get('DATABASE_URL'))
    )
