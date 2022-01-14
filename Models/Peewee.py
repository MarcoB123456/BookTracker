from peewee import Model, SqliteDatabase

db = SqliteDatabase("BookTracker.db")


class Peewee(Model):
    class Meta:
        database = db
