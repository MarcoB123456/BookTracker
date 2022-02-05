import json
import logging

import requests

logger = logging.getLogger(__name__)


def fetch_book_by_title(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    logger.info(f"Requesting information for book with title: {title}")
    return requests.get(url)


def fetch_book(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    logger.info(f"Requesting information for book with isbn: {isbn}")
    response = requests.get(url)
    logger.debug(f"Response received with status code: {response.status_code}")
    # TODO: Add functionality to search by title.
    if response.status_code != 200:
        logger.debug(f"Non successful response received with cause: {response.reason}")
        return None
    else:
        if response.json().get("items") is not None:
            return response


if __name__ == '__main__':
    # print(fetch_book("9781101965337").json())
    print(json.dumps(fetch_book_by_title("Boneshaker").json(), indent=4))

