from peewee import AutoField, TextField, IntegerField, ForeignKeyField, ManyToManyField
from playhouse.shortcuts import model_to_dict, dict_to_model

from Models.Author import Author
from Models.List import List
from Models.Peewee import Peewee


class Book(Peewee):
    book_id = AutoField(primary_key=True)
    ISBN = TextField(unique=True)
    title = TextField()
    authors = ManyToManyField(Author, backref="books")
    pages = IntegerField(null=True)
    rating = IntegerField(null=True)
    cover_image = TextField(null=True, default="Default.jpg")
    list = ForeignKeyField(List, null=True)

    def get_readings(self):
        return [read for read in self.readings]

    def get_authors(self):
        return [author for author in self.authors]

    def to_dict(self):
        return model_to_dict(self)

    @staticmethod
    def from_dict(dict_):
        return dict_to_model(Book, dict_)
