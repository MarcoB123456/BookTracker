from Service import BookService, ListService


def get_all_lists():
    return ListService.get_all_lists()


def get_all_books():
    return BookService.get_all_books()


def get_books_by_filter(filter_):
    return BookService.get_books_by_filter(filter_)


