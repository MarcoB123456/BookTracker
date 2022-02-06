import logging
from tkinter import messagebox as msg_box

from peewee import PeeweeException

from Models.Read import Read

logger = logging.getLogger(__name__)


def remove_all_by_book_id(book_id):
    try:
        query = Read.delete().where(Read.book_id == book_id)
        deleted_rows = query.execute()
        return deleted_rows
    except PeeweeException as exception:
        logger.debug(f"Exception while removing readings for book with id: {book_id}")
        msg_box.showerror("Error in ReadService", exception)


def add_reading(start_date, end_date, book_id):
    try:
        return Read.create(start_date=start_date, end_date=end_date, book_id=book_id)
    except PeeweeException as exception:
        logger.debug(
            f"Error while adding new Read object with start/end dates: {start_date}/{end_date} and book_id: {book_id} with message: {exception}")
        msg_box.showerror("Error in ReadService", exception)
