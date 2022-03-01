import tkinter as tk

from Controllers import ApplicationController
from Models.Book import Book
from UI.Custom.JSONVar import JSONVar
from UI.Dialogs.AddBookDialog import AddBookDialog
from UI.Dialogs.SettingsDialog import SettingsDialog
from UI.Widgets.BookTable import BookTable
from UI.Widgets.ListFrame import ListFrame
from UI.Widgets.PaginationFrame import Pagination
from UI.Widgets.SearchFrame import SearchFrame


class Application(tk.Tk):
    controller = ApplicationController

    def __init__(self):
        super().__init__()
        self.tk.call("source", "sun-valley.tcl")
        self.tk.call("set_theme", "dark")
        self.title("BookTracker")
        self.geometry(f"{int(self.winfo_screenwidth() * 0.8)}x{int(self.winfo_screenheight() * 0.6)}")

        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # Custom event's
        # TODO: Find a way to get rid of this. Constantly converting books to dict is not really an option,
        # but keeping everything in dicts doesn't really work with peewee all that well.
        self.bind("<<ListFilterUpdate>>", self.list_filter_changed)
        self.bind("<<PaginationUpdate>>", self.find_page_with_filter)

        # Variables
        self.books = []

        self.lists = JSONVar(self)
        self.lists.set(["None"])
        self.find_all_lists()

        # List filter
        self.left_frame = tk.Frame(self)
        self.left_frame.place(relx=0, rely=0, relwidth=0.2, relheight=0.8)

        self.list_frame = ListFrame(self.left_frame, self.lists)
        self.list_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.search_frame = SearchFrame(self.left_frame, self.lists)
        self.search_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.books_table = BookTable(self, self.books, self.lists)
        self.books_table.place(relx=0.2, rely=0, relheight=0.94, relwidth=0.8)

        # Switch frames
        self.search_frame_button = tk.Button(self, text="Search", command=self.search_frame.show)
        self.search_frame_button.place(relx=0, rely=0.9, relheight=0.1, relwidth=0.1)

        self.list_frame_button = tk.Button(self, text="List", command=self.list_frame.show)
        self.list_frame_button.place(relx=0.1, rely=0.9, relheight=0.1, relwidth=0.1)

        # Add book
        self.add_book_button = tk.Button(self, text="+", font="Helvetica 20 bold", command=self.open_add_book_dialog)
        self.add_book_button.place(relx=0.2, rely=0.94, relheight=0.06, relwidth=0.03)

        # Pagination frame
        self.pagination_frame = Pagination(self, self.books_table)
        self.pagination_frame.place(relx=0.45, rely=0.94, relheight=0.06, relwidth=0.3)

        # Open settings
        self.settings_button = tk.Button(self, text="⚙", font="Helvetica 14 bold", command=self.open_settings_dialog)
        self.settings_button.place(relx=0.98, rely=0.95, relheight=0.05, relwidth=0.02)

        # Find all books
        self.find_page_with_filter(1)

        self.mainloop()

    def list_filter_changed(self, *_):
        self.books, max_books = self._get_books_by_filter(1)
        self.pagination_frame.refresh_pagination(max_books)
        self.books_table.refresh_table(self.books)

    def find_page_with_filter(self, *_):
        self.books, max_books = self._get_books_by_filter()
        self.books_table.refresh_table(self.books)

    def _get_books_by_filter(self, page=None):
        if page is None:
            page = self.pagination_frame.get_current_page()

        return self.controller.get_books_by_filter(self.search_frame.get_filter(), page)

    def find_all_lists(self):
        all_lists = self.controller.get_all_lists()
        curr_lists = self.lists.get()

        for item in all_lists:
            curr_lists.append(item.name)

        self.lists.set(curr_lists)

    def open_settings_dialog(self):
        SettingsDialog(self)

    def open_add_book_dialog(self):
        result_book = JSONVar(self)
        result_book.set("")
        add_book_dialog = AddBookDialog(self, self.lists, result_book)
        self.wait_window(add_book_dialog)
        if result_book.get() != "":
            self.books.append(Book.from_dict(result_book.get()))
            self.books_table.refresh_table(self.books)

    def close_window(self):
        self.destroy()
