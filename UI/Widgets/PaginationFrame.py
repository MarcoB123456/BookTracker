import tkinter as tk
import math

from Controllers import ApplicationController
from UI.Widgets.BookTable import BookTable


class Pagination(tk.Frame):
    controller = ApplicationController

    def __init__(self, parent, books_table: BookTable):
        super().__init__(parent)

        # Variables
        self.books_table = books_table

        self.current_page_variable = tk.IntVar()
        self.current_page_variable.set(1)

        self.max_pages_variable = tk.IntVar()
        self.max_pages_variable.set(self.calc_max_pages(self.controller.get_book_count()))

        self.pages_variable = tk.StringVar()
        self.pages_variable.set(f"{self.current_page_variable.get()}/{self.max_pages_variable.get()}")

        # Previous page
        self.previous_button = tk.Button(self, text="<--", command=self.previous_page, font="Helvetica 18 bold")
        self.previous_button.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        # Page counter
        self.page_counter = tk.Label(self, textvariable=self.pages_variable, font="Helvetica 18 bold")
        self.page_counter.place(relx=0.4, rely=0, relwidth=0.2, relheight=1)

        # Next page
        self.next_button = tk.Button(self, text="-->", command=self.next_page, font="Helvetica 18 bold")
        self.next_button.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)

    def next_page(self):
        if self.current_page_variable.get() != self.max_pages_variable.get():
            self.current_page_variable.set(self.current_page_variable.get() + 1)
            self.pages_variable.set(f"{self.current_page_variable.get()}/{self.max_pages_variable.get()}")

            self.master.event_generate("<<PaginationUpdate>>")

    def previous_page(self):
        if self.current_page_variable.get() > 1:
            self.current_page_variable.set(self.current_page_variable.get() - 1)
            self.pages_variable.set(f"{self.current_page_variable.get()}/{self.max_pages_variable.get()}")

            self.master.event_generate("<<PaginationUpdate>>")

    def refresh_pagination(self, book_count):
        self.current_page_variable.set(1)
        self.max_pages_variable.set(self.calc_max_pages(book_count))
        self.pages_variable.set(f"{self.current_page_variable.get()}/{self.max_pages_variable.get()}")

    def get_current_page(self):
        return self.current_page_variable.get()

    @staticmethod
    def calc_max_pages(book_count):
        if book_count == 0:
            return 1
        else:
            return math.ceil(book_count / 20)
