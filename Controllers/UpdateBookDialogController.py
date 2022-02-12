import logging
import os
import shutil
from tkinter import filedialog, messagebox

from Definitions import ROOT_PATH
from Service import ReadService, BookService, ListService, AuthorService

logger = logging.getLogger(__name__)


def save_book(book_id, title, author_list, pages, rating, list_name, reading_list):
    # Unsure how to update reading list so just remove all of them first
    ReadService.remove_all_by_book_id(book_id)
    # Add all readings
    for reading in reading_list:
        start_date, end_date = reading.split(" - ")
        ReadService.add_reading(start_date, end_date, book_id)

    # Unsure how to update author list so just remove all of them first
    BookService.remove_all_authors_from_book(book_id)
    # Add all readings
    for author in author_list:
        author = AuthorService.get_or_create_author(author)
        BookService.add_author_to_book_with_id(book_id, author[0])

    if list_name == "None":
        list_ = None
    else:
        list_ = ListService.get_list_by_name(list_name)

    # An index of zero means no rating.
    if rating == 0:
        rating = None

    # Return amount of updated rows
    return BookService.update_book(book_id, title, pages, rating, list_)


def upload_cover_image():
    src_path = filedialog.askopenfilename(filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")))
    filename = src_path.split("/")[-1]
    if not os.path.isfile(f"{ROOT_PATH}\\Images\\Covers\\{filename}"):
        messagebox.showerror("File already exists", f"Cover image with name: {filename} already exists.")
        return None

    logger.debug(f"Attempting to copy file: {src_path} to Covers directory")
    shutil.copy(src_path, ROOT_PATH + "\\Images\\Covers")
    return filename


def get_book(isbn):
    return BookService.get_book_by_isbn(isbn)
