import logging

from Controllers import GoogleBooksApi, BookTrackerUtils, ISBNValidator
from Service import BookService, ReadService, AuthorService

logger = logging.getLogger(__name__)


def add_book(isbn, list_name, rating, start_date, end_date, warning_label):
    # Check if ISBN is valid
    if not ISBNValidator.is_valid_isbn(isbn):
        warning_label.set("ISBN is invalid")
        return None

    # Check if book with isbn input was already added
    if BookService.book_exists(isbn):
        warning_label.set("Book with isbn already exists")
        return None

    # Fetch book information from api
    result = GoogleBooksApi.fetch_book(isbn)
    if result is None:
        logger.info(f"No match was found for isbn: {isbn}")
        warning_label.set("No match was found")
        return None

    json_result = result.json()
    for item in json_result['items'][0]['volumeInfo']['industryIdentifiers']:
        if item['type'] == "ISBN_13":
            isbn = item['identifier']
    title = json_result['items'][0]['volumeInfo']['title']
    authors = json_result['items'][0]['volumeInfo']['authors']
    pages = json_result['items'][0]['volumeInfo']['pageCount']

    # Save cover image
    if "imageLinks" in json_result['items'][0]['volumeInfo']:
        cover_image = BookTrackerUtils.save_image(
            json_result['items'][0]['volumeInfo']['imageLinks']['thumbnail'], isbn)

    # Add book to the database
    new_book = BookService.add_book(isbn, title, pages, cover_image, rating, list_name)

    # Add authors to book
    for author in authors:
        author = AuthorService.get_or_create_author(author)
        BookService.add_author_to_book(new_book, author[0])

    # Add read to book if available
    if start_date is not None and new_book is not None:
        ReadService.add_reading(start_date, end_date, new_book.book_id)

    return new_book
