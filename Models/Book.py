from peewee import AutoField, TextField, IntegerField, ForeignKeyField
from playhouse.shortcuts import model_to_dict, dict_to_model

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

    def to_dict(self):
        return model_to_dict(self)

    @staticmethod
    def from_dict(dict_):
        return dict_to_model(Book, dict_)
