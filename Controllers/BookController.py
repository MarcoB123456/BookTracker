import logging
import tkinter.messagebox as msg_box

from peewee import PeeweeException, DoesNotExist

from Models.Book import Book
from Models.List import List

logger = logging.getLogger(__name__)


def get_all_books():
    logger.info("Querying all books")
    query = Book.select()
    result = [book for book in query]
    return result


def get_books_by_list(list_name):
    logger.info("Querying books by list")
    query = Book.select().join(List).where(List.name == list_name)
    result = [book for book in query]
    return result


def get_books_by_filter(filter_):
    logger.info("Querying books by filter")
    logger.debug(f"Filter used is: {filter_}")

    query = Book.select()

    if filter_.list_name is not None and filter_.list_name != "None":
        query = query.join(List).where(List.name == filter_.list_name)
    result = [book for book in query]
    return result


def get_book_by_isbn(isbn):
    logger.info("Querying book by isbn")

    try:
        book = Book.get(Book.ISBN == isbn)
        return book
    except DoesNotExist as exception:
        logger.debug(f"Book with isbn: {isbn} does not exist")
        msg_box.showerror("Error in BookController", exception)


def get_books_by_title(title):
    # TODO: Implement this
    raise NotImplementedError("Not yet implemented")


def get_books_by_author(author):
    # TODO: Implement this
    raise NotImplementedError("Not yet implemented")


def add_book(isbn, title, author, pages, rating=None, list_name=None):
    logger.info("Adding book to database")
    logger.debug(
        f"Adding values isbn: {isbn}, title: {title}, author: {author}, pages: {pages}, rating: {rating}, list: {list_name}")
    try:
        if list_name is None or list_name == "None":
            new_book = Book.create(ISBN=isbn, title=title, author=author, pages=pages, rating=rating)
        else:
            new_book = Book.create(ISBN=isbn, title=title, author=author, pages=pages, rating=rating,
                                   list=List.get(List.name == list_name).list_id)
        return new_book
    except PeeweeException as exception:
        logger.warning(
            f"""Error while inserting book with params isbn: {isbn}, title: {title}, author: {author}, pages: {pages}
            ,rating: {rating}, list: {list_name}, with message: {exception}""")
        msg_box.showerror("Error in BookController", exception)


def book_exists(isbn):
    logger.info(f"Checking if book with isbn: {isbn} already exists")
    try:
        Book.get(ISBN=isbn)
        logger.debug(f"Book with isbn: {isbn} already exists")
        return True
    except DoesNotExist:
        logger.debug(f"Book with isbn: {isbn} does not yet exist")
        return False


def remove_book(isbn):
    logger.info(f"Removing book with isbn: {isbn} from the database")
    try:
        book = Book.get(Book.ISBN == isbn)
        # Returns amount of deleted rows
        removed_rows = book.delete_instance()
        logger.debug(f"Removed {removed_rows} amount of rows")
        return removed_rows
    except DoesNotExist as exception:
        logger.warning(
            f"Error while deleting book with isbn: {isbn}, with message: {exception}")
        msg_box.showerror("Error in BookController", exception)


def update_book_rating(isbn, rating):
    logger.info(f"Updating rating: {rating} for book with isbn: {isbn}")
    try:
        query = Book.update(rating=rating).where(Book.ISBN == isbn)
        # Returns updated rows
        updated_rows = query.execute()
        logger.debug(f"Updated {updated_rows} rows")
        return updated_rows
    except PeeweeException as exception:
        logger.warning(
            f"""Error while updating rating: {rating} for book with isbn: {isbn}, message: {exception}""")
        msg_box.showerror("Error in BookController", exception)


def update_book(new_book: Book):
    logger.info(f"Updating book")
    try:
        old_book: Book = Book.get_by_id(new_book.book_id)

        old_book.title = new_book.title
        old_book.author = new_book.author
        old_book.pages = new_book.pages
        if new_book.list.name is None or new_book.list.name == "None":
            old_book.list = None
        else:
            old_book.list = List.get(List.name == new_book.list.name)
        old_book.rating = new_book.rating

        updated_rows = old_book.save()
        return updated_rows
    except DoesNotExist as exception:
        logger.warning(
            f"""Error while updating book with isbn: {new_book.ISBN} """)
        msg_box.showerror("Error in BookController", exception)


def move_book_to_list(isbn, list_name):
    logger.info(f"Moving book with isbn: {isbn} to list with name: {list_name}")
    try:
        query = Book.update(list=List.get(name=list_name).list_id).where(Book.ISBN == isbn)
        query.execute()
    except PeeweeException as exception:
        logger.warning(
            f"""Error while moving book with isbn: {isbn} to list with name: {list_name}, message: {exception}""")
        msg_box.showerror("Error in BookController", exception)


def remove_book_from_list(isbn):
    logger.info(f"Removing book with isbn: {isbn} from list.")
    try:
        query = Book.update(list=None).where(Book.ISBN == isbn)
        updated_rows = query.execute()
        logger.debug(f"Updated {updated_rows} rows")
        return updated_rows
    except PeeweeException as exception:
        logger.warning(
            f"""Error while removing book with isbn: {isbn} from list, message: {exception}""")
        msg_box.showerror("Error in BookController", exception)


def remove_all_books_from_list(list_name):
    logger.info(f"Remove all books from list with name: {list_name}")
    try:
        query = Book.update(list=None).where(List.get(name=list_name).list_id)
        updated_rows = query.execute()
        logger.debug(f"Updated {updated_rows} rows")
        return updated_rows
    except PeeweeException as exception:
        logger.warning(
            f"""Error while removing all books from list with name: {list_name}, message: {exception}""")
        msg_box.showerror("Error in BookController", exception)
