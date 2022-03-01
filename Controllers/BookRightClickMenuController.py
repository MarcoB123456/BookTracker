import logging
from tkinter import messagebox as msg_box

from Controllers import BookTrackerUtils
from Service import BookService, ReadService

logger = logging.getLogger(__name__)


def delete_book(isbn, title):
    logger.debug(f"Started deletion process for a book with name: {title}")
    if msg_box.askyesno("Delete book", f"Are you sure you want to delete: {title}"):
        logger.debug(
            f"Confirmed deletion of book with isbn: {isbn}, title: {title}")
        book_id = BookService.remove_book(isbn, title)

        ReadService.remove_all_by_book_id(book_id)
        if isbn != "":
            BookTrackerUtils.remove_image(isbn)
        return True


def move_book_to_list(isbn, list_name):
    if list_name is None or list_name == "None":
        return BookService.remove_list_from_book(isbn)
    else:
        return BookService.move_book_to_list(isbn, list_name)


def update_rating(isbn, rating):
    return BookService.update_book_rating(isbn, rating)
