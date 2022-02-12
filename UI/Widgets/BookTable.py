import tkinter as tk
from tkinter import ttk

from Controllers.BookTrackerUtils import build_rating
from UI.Widgets.BookRightClickMenu import BookRightClickMenu


class BookTable(ttk.Treeview):
    book_list_columns = ('ISBN', 'Title', 'Author', 'Pages', 'Rating', 'Start date', 'End date')

    def __init__(self, parent, books, lists):

        self.books = books
        self.lists = lists

        super().__init__(parent, columns=self.book_list_columns, selectmode='browse')
        # Build book list
        self.column("#0", width=20, stretch=tk.NO)
        self.column("ISBN", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.column("Title", stretch=tk.YES, anchor=tk.CENTER, width=300)
        self.column("Author", stretch=tk.NO, anchor=tk.CENTER, width=200)
        self.column("Pages", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.column("Rating", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.column("Start date", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.column("End date", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.heading("#0", text="")
        for column in self.book_list_columns:
            self.heading(column, text=column,
                         command=lambda _column=column: self.treeview_sort_column(self, _column,
                                                                                  False))

        # Create right click menu
        self.bind("<Button-3>", self.open_book_right_click_menu)

        self.populate_book_list()

    def populate_book_list(self):
        self.delete(*self.get_children())
        for book in self.books:

            readings = book.get_readings()
            start_date, end_date = '', ''
            if readings:
                first_read = readings.pop(0)
                start_date, end_date = first_read.start_date, first_read.end_date

            authors = book.get_authors()
            author = ''
            if authors:
                author = authors.pop(0).name

            row_id = self.add_book_list_item(book, author, start_date, end_date)

            # Check if readings or authors has at least one item left
            while readings or authors:
                start_date = ''
                end_date = ''
                author = ''
                if readings:
                    read = readings.pop(0)
                    start_date, end_date = read.start_date, read.end_date
                if authors:
                    author = authors.pop(0).name
                self.add_book_child_item(book, author, start_date, end_date, row_id)

    def add_book_list_item(self, book, author='', start_date='', end_date=''):
        return self.insert(parent='', index=tk.END, values=(
            book.ISBN, book.title, author, book.pages, build_rating(book.rating), start_date,
            end_date), tags=(self.list_not_none(book),))

    def add_book_child_item(self, book, author, start_date, end_date, row_id):
        return self.insert(parent=row_id, index=tk.END, values=('', '', author, '', '', start_date, end_date),
                           tags=(self.list_not_none(book),))

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def open_book_right_click_menu(self, event):
        selected_item_id = self.identify_row(event.y)
        if self.parent(selected_item_id) != '':
            selected_item_id = self.parent(selected_item_id)
        self.selection_set(selected_item_id)
        selected_item = self.item(selected_item_id)
        BookRightClickMenu(self, event, selected_item, self.lists)

    def refresh_table(self, books):
        self.books = books
        self.populate_book_list()

    @staticmethod
    def list_not_none(book):
        if book.list is None:
            return "None"
        else:
            return book.list.name

    @staticmethod
    def has_one_read_minimum(readings):
        if readings:
            return readings[0].start_date, readings[0].end_date
        else:
            return '', ''

    @staticmethod
    def has_one_author_minimum(author):
        if author:
            return author[0].name
        else:
            return ''
