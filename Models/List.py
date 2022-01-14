from peewee import AutoField, TextField

from Models.Peewee import Peewee


class List(Peewee):
    list_id = AutoField(primary_key=True)
    name = TextField(unique=True)
