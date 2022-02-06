from Service import BookService, ListService


def get_all_lists():
    return ListService.get_all_lists()


def get_all_books():
    return BookService.get_all_books()


def get_books_by_filter(filter_):
    return BookService.get_books_by_filter(filter_)


def list_not_none(book):
    if book.list is None:
        return "None"
    else:
        return book.list.name


def has_one_read_minimum(readings):
    if readings:
        return readings[0].start_date, readings[0].end_date
    else:
        return '', ''
