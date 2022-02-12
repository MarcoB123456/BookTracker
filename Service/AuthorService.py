import logging

from peewee import DoesNotExist

from Models.Author import Author

logger = logging.getLogger(__name__)


def get_or_create_author(name):
    return Author.get_or_create(name=name)


def add_author(name):
    return Author.create(name=name)


def remove_author(name):
    logger.info(f"Removing author with name {name}")
    try:
        author = Author.get(Author.name == name)
        removed_rows = author.delete_instance()
        return removed_rows
    except DoesNotExist as exception:
        logger.debug(f"Error while removing author with name: {name} and exception: {exception}")
