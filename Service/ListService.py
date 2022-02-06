import logging
import tkinter.messagebox as msg_box

from peewee import PeeweeException, DoesNotExist

from Models.List import List

logger = logging.getLogger(__name__)


def get_all_lists():
    logger.info("Querying all lists")
    query = List.select()
    result = [item for item in query]
    return result


def add_list(list_name):
    logger.info(f"Adding list with name: {list_name}")
    try:
        new_list = List.create(name=list_name)
        return new_list
    except PeeweeException as exception:
        logger.warning(
            f"""Error while adding list with name: {list_name} , with message: {exception}""")
        msg_box.showerror("Error in ListService", exception)


def update_list(new_name, old_name):
    logger.info(f"Updating list with name: {old_name} to: {new_name}")
    try:
        query = List.update(name=new_name).where(List.name == old_name)
        updated_rows = query.execute()
        logger.debug(f"Updated {updated_rows} rows")
        return updated_rows
    except DoesNotExist as exception:
        logger.warning(
            f"Error while updating list with name: {old_name} to: {new_name}, with message: {exception}")
        msg_box.showerror("Error in ListService", exception)


def remove_list(list_name):
    logger.info(f"Removing book with name: {list_name}")
    try:
        list_ = List.get(name=list_name)
        deleted_rows = list_.delete_instance()
        logger.debug(f"Deleted {deleted_rows} rows")
        return deleted_rows
    except DoesNotExist as exception:
        logger.warning(
            f"Error while deleting list with name: {list_name}, with message: {exception}")
        msg_box.showerror("Error in ListService", exception)


def get_list_by_name(name):
    try:
        return List.get(List.name == name)
    except DoesNotExist as exception:
        logger.warning(
            f"Error getting list with name: {name}, with message: {exception}")
        msg_box.showerror("Error in ListService", exception)

