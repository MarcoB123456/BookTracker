from peewee import Model, SqliteDatabase
from Definitions import ROOT_PATH

db = SqliteDatabase(f"{ROOT_PATH}/BookTracker.db")


class Peewee(Model):
    class Meta:
        database = db
