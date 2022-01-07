import sqlite3
import logging
from Models.List import List

logger = logging.getLogger(__name__)


def get_connection():
    logger.debug("Opening database connection")
    return sqlite3.connect("BookTracker.db")


def get_all_lists():
    conn = get_connection()
    logger.info("Querying all lists")
    cursor = conn.execute("SELECT Name FROM List")
    result = [List(None, item[0]) for item in cursor.fetchall()]
    conn.close()
    return result


def get_list_by_name(name):
    # TODO: Implement this
    raise NotImplementedError("Not yet implemented")


def move_book_to_list(isbn, list_name):
    conn = get_connection()
    logger.info(f"Moving book with isbn: {isbn} to list with name: {list_name}")
    conn.execute(
        f"UPDATE Book SET ListId = (SELECT Id FROM List WHERE Name = '{list_name}') WHERE ISBN = '{isbn}'")
    try:
        conn.commit()
        conn.close()
    except sqlite3.Error as msg:
        logger.warning(
            f"""Error while moving book with isbn: {isbn} to list with name: {list_name}, message: {msg}""")
        conn.close()
        return msg


def remove_book_from_list(isbn):
    conn = get_connection()
    logger.info(f"Removing book with isbn: {isbn} from list.")
    conn.execute(
        f"UPDATE Book SET ListId = '{None}' WHERE ISBN = '{isbn}'")
    try:
        conn.commit()
        conn.close()
    except sqlite3.Error as msg:
        logger.warning(
            f"""Error while removing book with isbn: {isbn} from list, message: {msg}""")
        conn.close()
        return msg
