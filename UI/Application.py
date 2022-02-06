import tkinter as tk
from tkinter import ttk

from Controllers import ApplicationController
from Controllers.BookTrackerUtils import build_rating
from Models.Book import Book
from UI.Custom.JSONVar import JSONVar
from UI.Dialogs.AddBookDialog import AddBookDialog
from UI.Widgets.BookRightClickMenu import BookRightClickMenu
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
        # TODO: Find a way to get rid of this. Constantly coverting books to dict is not really an option,
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

        # Build book list
        book_list_columns = ('ISBN', 'Title', 'Author', 'Pages', 'Rating', 'Start date', 'End date')
        self.book_list = ttk.Treeview(self, columns=book_list_columns, selectmode='browse')
        self.book_list.column("#0", width=20, stretch=tk.NO)
        self.book_list.column("ISBN", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.book_list.column("Title", stretch=tk.YES, anchor=tk.CENTER, width=300)
        self.book_list.column("Author", stretch=tk.NO, anchor=tk.CENTER, width=200)
        self.book_list.column("Pages", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.book_list.column("Rating", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.book_list.column("Start date", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.book_list.column("End date", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.book_list.heading("#0", text="")
        for column in book_list_columns:
            self.book_list.heading(column, text=column,
                                   command=lambda _column=column: self.treeview_sort_column(self.book_list, _column,
                                                                                            False))

        # Create right click menu
        self.book_list.bind("<Button-3>", self.open_book_right_click_menu)

        self.book_list.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)
        self.populate_book_list()

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
        self.populate_book_list()

    def populate_book_list(self):
        self.book_list.delete(*self.book_list.get_children())
        for book in self.books:
            start_date, end_date = self.controller.has_one_read_minimum(book.get_readings())
            row_id = self.add_book_list_item(book, start_date, end_date)
            if len(book.get_readings()) > 1:
                readings = book.get_readings()
                readings.pop(0)
                for read in readings:
                    self.add_book_child_item(book, read.start_date, read.end_date, row_id)

    def add_book_list_item(self, book, start_date='', end_date=''):
        return self.book_list.insert(parent='', index=tk.END, values=(
            book.ISBN, book.title, book.author, book.pages, build_rating(book.rating), start_date,
            end_date), tags=(self.controller.list_not_none(book),))

    def add_book_child_item(self, book, start_date, end_date, row_id):
        return self.book_list.insert(parent=row_id, index=tk.END, values=('', '', '', '', '', start_date, end_date),
                                     tags=(self.controller.list_not_none(book),))



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
            self.populate_book_list()

    def open_book_right_click_menu(self, event):
        selected_item_id = self.book_list.identify_row(event.y)
        if self.book_list.parent(selected_item_id) != '':
            selected_item_id = self.book_list.parent(selected_item_id)
        self.book_list.selection_set(selected_item_id)
        selected_item = self.book_list.item(selected_item_id)
        BookRightClickMenu(self, event, selected_item, self.lists)

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: \
            self.treeview_sort_column(tv, col, not reverse))
