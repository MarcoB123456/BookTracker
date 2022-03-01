import logging
from os.path import exists
from pathlib import Path

from Models.Author import Author
from Models.Book import Book
from Models.List import List
from Models.Peewee import db
from Models.Read import Read
from UI.Application import Application


def log_init():
    logging.basicConfig(filename="main.log",
                        filemode="a",
                        format="%(asctime)s | %(levelname)s | %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.DEBUG)


def db_init():
    if not Path("BookTracker.db").exists():
        BookAuthor = Book.authors.get_through_model()

        db.create_tables([List, Book, Read, Author, BookAuthor])

        List.create(name="Reading")
        List.create(name="To-read")
        List.create(name="Finished")
        List.create(name="Dropped")


if __name__ == '__main__':
    log_init()
    db_init()
    Application()
