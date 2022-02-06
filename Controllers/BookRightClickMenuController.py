import logging
from tkinter import messagebox as msg_box

from Controllers import BookTrackerUtils
from Service import BookService

logger = logging.getLogger(__name__)


def delete_book(isbn, name):
    logger.debug(f"Started deletion process for a book with name: {name}")
    if msg_box.askyesno("Delete book", f"Are you sure you want to delete: {name}"):
        logger.debug(
            f"Confirmed deletion of book with isbn: {isbn}, title: {name}")
        removed_rows = BookService.remove_book(isbn)
        if removed_rows is not None:
            BookTrackerUtils.remove_image(isbn)
            return True


def move_book_to_list(isbn, list_name):
    if list_name is None or list_name == "None":
        return BookService.remove_book_from_list(isbn)
    else:
        return BookService.move_book_to_list(isbn, list_name)


def update_rating(isbn, rating):
    return BookService.update_book_rating(isbn, rating)
