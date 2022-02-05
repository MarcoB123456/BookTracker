from peewee import AutoField, DateField, ForeignKeyField

from Models.Book import Book
from Models.Peewee import Peewee


class Read(Peewee):

    read_id = AutoField(primary_key=True)
    start_date = DateField(null=False)
    end_date = DateField(null=True, formats="DD-MM-YYYY")
    book_id = ForeignKeyField(Book, backref="readings", null=True)
