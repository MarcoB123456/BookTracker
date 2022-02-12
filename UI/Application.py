import tkinter as tk

from Controllers import ApplicationController
from Models.Book import Book
from UI.Custom.JSONVar import JSONVar
from UI.Dialogs.AddBookDialog import AddBookDialog
from UI.Widgets.BookTable import BookTable
from UI.Widgets.ListFrame import ListFrame
from UI.Widgets.SearchFrame import SearchFrame


class Application(tk.Tk):
    controller = ApplicationController

    def __init__(self):
        super().__init__()
        self.tk.call("source", "sun-valley.tcl")
        self.tk.call("set_theme", "dark")
        self.title("BookTracker")
        self.geometry(f"{int(self.winfo_screenwidth() * 0.8)}x{int(self.winfo_screenheight() * 0.6)}")

        # Custom event's
        # TODO: Find a way to get rid of this. Constantly converting books to dict is not really an option,
        # but keeping everything in dicts doesn't really work with peewee all that well.
        self.bind("<<BookUpdate>>", self.find_all_books_with_filter)

        # Variables
        self.books = []
        self.find_all_books()

        self.lists = JSONVar(self)
        self.lists.set(["None"])
        self.find_all_lists()

        # Build list filter
        self.left_frame = tk.Frame(self)
        self.left_frame.place(relx=0, rely=0, relwidth=0.2, relheight=0.8)

        self.list_frame = ListFrame(self.left_frame, self.lists)
        self.list_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.search_frame = SearchFrame(self.left_frame, self.lists)
        self.search_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.books_table = BookTable(self, self.books, self.lists)
        self.books_table.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)

        # Switch frames buttons
        self.search_frame_button = tk.Button(self, text="Search", command=self.search_frame.show)
        self.search_frame_button.place(relx=0, rely=0.9, relheight=0.1, relwidth=0.1)

        self.list_frame_button = tk.Button(self, text="List", command=self.list_frame.show)
        self.list_frame_button.place(relx=0.1, rely=0.9, relheight=0.1, relwidth=0.1)

        # Build add button
        self.add_book_button = tk.Button(self, text="+", font="Helvetica 20 bold", command=self.open_add_book_dialog)
        self.add_book_button.place(relx=0.2, rely=0.93, relheight=0.07, relwidth=0.07)
        self.mainloop()

    def find_all_books(self):
        self.books = self.controller.get_all_books()

    def find_all_books_with_filter(self, event=None):
        if event is None:
            self.books = self.controller.get_all_books()
        else:
            self.books = self.controller.get_books_by_filter(self.search_frame.get_filter())
        self.books_table.refresh_table(self.books)

    def find_all_lists(self):
        all_lists = self.controller.get_all_lists()
        curr_lists = self.lists.get()

        for item in all_lists:
            curr_lists.append(item.name)

        self.lists.set(curr_lists)

    def open_add_book_dialog(self):
        result_book = JSONVar(self)
        result_book.set("")
        add_book_dialog = AddBookDialog(self, self.lists, result_book)
        self.wait_window(add_book_dialog)
        if result_book.get() != "":
            self.books.append(Book.from_dict(result_book.get()))
            self.books_table.refresh_table(self.books)
