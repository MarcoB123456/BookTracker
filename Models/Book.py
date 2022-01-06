from Models.List import List


class Book:

    def __init__(self, book_id, ISBN, title, author, pages, rating, list_id, list_name):
        self.book_id = book_id
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.pages = pages
        self.rating = rating
        self.list = List(list_id, list_name)

