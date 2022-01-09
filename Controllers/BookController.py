import sqlite3
import logging
from Models.Book import Book

logger = logging.getLogger(__name__)


def get_connection():
    logger.debug("Opening database connection")
    return sqlite3.connect("BookTracker.db")


def get_all_books():
    conn = get_connection()
    logger.info("Querying all books")
    cursor = conn.execute("""SELECT Book.Id, ISBN, Title, Author, Pages, Rating, ListId, Name 
                                FROM Book LEFT JOIN List ON Book.ListId = List.Id""")
    result = [Book(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]) for item in
              cursor.fetchall()]
    conn.close()
    return result


def get_books_by_list(list):
    conn = get_connection()
    logger.info("Querying books by list")
    cursor = conn.execute(
        f"""SELECT Book.Id, ISBN, Title, Author, Pages, Rating, ListId, Name 
            FROM Book INNER JOIN List ON Book.ListId = List.Id WHERE List.Name = '{list}'""")
    result = [Book(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]) for item in
              cursor.fetchall()]
    conn.close()
    return result


def get_books_by_filter(filter):
    conn = get_connection()
    logger.info("Querying books by filter")
    logger.debug(f"Filter used is: {filter}")

    query = "SELECT Book.Id, ISBN, Title, Author, Pages, Rating, ListId, Name FROM Book LEFT JOIN List ON Book.ListId = List.Id "
    if filter.list_name is not None and filter.list_name != "None":
        query += f"WHERE List.Name = '{filter.list_name}' "
    cursor = conn.execute(query)
    result = [Book(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]) for item in
              cursor.fetchall()]
    conn.close()
    return result


def get_book_by_isbn(isbn):
    # TODO: Implement this
    raise NotImplementedError("Not yet implemented")


def get_books_by_title(title):
    # TODO: Implement this
    raise NotImplementedError("Not yet implemented")


def get_books_by_author(author):
    # TODO: Implement this
    raise NotImplementedError("Not yet implemented")


def add_book(isbn, title, author, pages):
    conn = get_connection()
    logger.info("Adding book to database")
    logger.debug(f"Adding values isbn: {isbn}, title: {title}, author: {author}, pages: {pages}")
    conn.execute(
        f"INSERT INTO Book ('ISBN', 'Title', 'Author', 'Pages') VALUES (?, ?, ?, ?)", (isbn, title, author, pages))
    try:
        conn.commit()
        conn.close()
    except sqlite3.Error as msg:
        logger.warning(
            f"""Error while inserting book with params isbn: {isbn}, title: {title}, author: {author}, pages: {pages}
                , with message: {msg}""")
        conn.close()
        return msg


def book_exists(isbn):
    conn = get_connection()
    logger.info(f"Checking if book with isbn: {isbn} already exists")
    cursor = conn.execute("SELECT ISBN FROM Book WHERE ISBN = ?", (isbn,))
    if cursor.fetchone() is not None:
        logger.debug(f"Book with isbn: {isbn} already exists")
        conn.close()
        return True
    else:
        logger.debug(f"Book with isbn: {isbn} does not yet exist")
        conn.close()
        return False


def remove_book(isbn):
    conn = get_connection()
    logger.info(f"Removing book with isbn: {isbn} from the database")
    conn.execute("DELETE FROM book WHERE isbn= ?", (isbn,))
    try:
        conn.commit()
        conn.close()
    except sqlite3.Error as msg:
        logger.warning(
            f"Error while deleting book with isbn: {isbn}, with message: {msg}")
        conn.close()
        return msg


def update_book_rating(isbn, rating):
    conn = get_connection()
    logger.info(f"Updating rating: {rating} for book with isbn: {isbn}")
    conn.execute(
        "UPDATE Book SET Rating = ? WHERE ISBN = ?", (rating, isbn))
    try:
        conn.commit()
        conn.close()
    except sqlite3.Error as msg:
        logger.warning(
            f"""Error while updating rating: {rating} for book with isbn: {isbn}, message: {msg}""")
        conn.close()
        return msg


def remove_all_books_from_list(list_name):
    conn = get_connection()
    logger.info(f"Remove all books from list with name: {list_name}")
    conn.execute("UPDATE Book SET ListId = ? WHERE ListId = (SELECT List.Id FROM List WHERE Name = ?)",
                 (None, list_name))
    try:
        conn.commit()
        conn.close()
    except sqlite3.Error as msg:
        logger.warning(
            f"""Error while removing all books from list with name: {list_name}, message: {msg}""")
        conn.close()
        return msg