import logging

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
        # This returns the list object. Might be able to do some stuff with it.
        List.create(name=list_name)
    except PeeweeException as msg:
        logger.warning(
            f"""Error while adding list with name: {list_name} , with message: {msg}""")
        return msg


def update_list(new_name, old_name):
    logger.info(f"Updating list with name: {old_name} to: {new_name}")
    try:
        query = List.update(name=new_name).where(List.name == old_name)
        # This returns amount of effected rows.
        query.execute()
    except DoesNotExist as msg:
        logger.warning(
            f"Error while updating list with name: {old_name} to: {new_name}, with message: {msg}")
        return msg


def remove_list(list_name):
    logger.info(f"Removing book with name: {list_name}")
    try:
        list_ = List.get(name=list_name)
        # This returns effected rows
        list_.delete_instance()
    except DoesNotExist as msg:
        logger.warning(
            f"Error while deleting list with name: {list_name}, with message: {msg}")
        return msg


def get_list_by_name(name):
    # TODO: Implement this
    raise NotImplementedError("Not yet implemented")
