from peewee import AutoField, TextField, IntegerField, ForeignKeyField

from Models.List import List
from Models.Peewee import Peewee


class Book(Peewee):
    book_id = AutoField(primary_key=True)
    ISBN = TextField(unique=True)
    title = TextField()
    author = TextField(null=True)
    pages = IntegerField(null=True)
    rating = IntegerField(null=True)
    list = ForeignKeyField(List, null=True)

    def get_readings(self):
        return [read for read in self.readings]