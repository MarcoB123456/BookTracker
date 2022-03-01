from Service import BookService, ListService


def get_all_lists():
    return ListService.get_all_lists()


def get_book_count():
    return BookService.get_book_count()


def get_all_books_by_page(page):
    books = BookService.get_all_books_by_page(page)
    max_books = BookService.get_book_count()
    return books, max_books


def get_books_by_filter(filter_, page):
    return BookService.get_books_by_filter(filter_, page)
