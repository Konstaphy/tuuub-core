from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    'postgres',
    user='postgres',
    password='p123p123p123',

    host='95.182.121.35',
    port='5432'
)
