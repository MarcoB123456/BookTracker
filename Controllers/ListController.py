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


def add_list(list_name):
    conn = get_connection()
    logger.info(f"Adding list with name: {list_name}")
    conn.execute(
        f"INSERT INTO List ('Name') VALUES (?)", (list_name,))
    try:
        conn.commit()
        conn.close()
    except sqlite3.Error as msg:
        logger.warning(
            f"""Error while adding list with name: {list_name} , with message: {msg}""")
        conn.close()
        return msg


def update_list(new_name, old_name):
    conn = get_connection()
    logger.info(f"Updating list with name: {old_name} to: {new_name}")
    conn.execute("UPDATE List SET Name = ? WHERE Name = ?", (new_name, old_name))
    try:
        conn.commit()
        conn.close()
    except sqlite3.Error as msg:
        logger.warning(
            f"Error while updating list with name: {old_name} to: {new_name}, with message: {msg}")
        conn.close()
        return msg


def remove_list(list_name):
    conn = get_connection()
    logger.info(f"Removing book with name: {list_name}")
    conn.execute("DELETE FROM List WHERE Name = ?", (list_name,))
    try:
        conn.commit()
        conn.close()
    except sqlite3.Error as msg:
        logger.warning(
            f"Error while deleting list with name: {list_name}, with message: {msg}")
        conn.close()
        return msg


def get_list_by_name(name):
    # TODO: Implement this
    raise NotImplementedError("Not yet implemented")


def move_book_to_list(isbn, list_name):
    conn = get_connection()
    logger.info(f"Moving book with isbn: {isbn} to list with name: {list_name}")
    conn.execute(
        "UPDATE Book SET ListId = (SELECT Id FROM List WHERE Name = ?) WHERE ISBN = ?", (list_name, isbn))
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
        "UPDATE Book SET ListId = ? WHERE ISBN = ?", (None, isbn))
    try:
        conn.commit()
        conn.close()
    except sqlite3.Error as msg:
        logger.warning(
            f"""Error while removing book with isbn: {isbn} from list, message: {msg}""")
        conn.close()
        return msg
