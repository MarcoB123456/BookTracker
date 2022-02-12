from peewee import TextField, AutoField

from Models.Peewee import Peewee


class Author(Peewee):
    author_id = AutoField(primary_key=True)
    name = TextField(unique=True)
