import tkinter as tk
from tkinter import ttk

from Controllers import BookController, ListController
from Models.Filter import Filter
from UI.AddBookDialog import AddBookDialog
from UI.BookRightClickMenu import BookRightClickMenu
from UI.ListFrame import ListFrame
from UI.SearchFrame import SearchFrame


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tk.call("source", "sun-valley.tcl")
        self.tk.call("set_theme", "dark")
        self.title("BookTracker")
        self.geometry("1000x500")

        # Custom event's
        self.bind("<<BookUpdate>>", self.find_all_books_with_filter)
        self.bind("<<ListUpdate>>", self.update_lists)

        # Variables
        self.books = []
        self.find_all_books()

        self.lists = ["None"]
        self.find_all_lists()

        # Build list filter
        self.left_frame = tk.Frame(self)
        self.left_frame.place(relx=0, rely=0, relwidth=0.2, relheight=0.8)

        self.list_frame = ListFrame(self.left_frame, self.lists)
        self.list_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.search_frame = SearchFrame(self.left_frame, self.lists)
        self.search_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Build book list
        book_list_columns = ('ISBN', 'Title', 'Author', 'Pages', 'Rating')
        self.book_list = ttk.Treeview(self, columns=book_list_columns, selectmode='browse')
        self.book_list.column("#0", width=0, stretch=tk.NO)
        self.book_list.column("ISBN", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.book_list.column("Title", stretch=tk.YES, anchor=tk.CENTER, width=300)
        self.book_list.column("Author", stretch=tk.NO, anchor=tk.CENTER, width=200)
        self.book_list.column("Pages", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
        self.book_list.column("Rating", stretch=tk.NO, anchor=tk.CENTER, minwidth=100, width=100)
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
        self.books = BookController.get_all_books()

    def find_all_books_with_filter(self, event=None):
        if event is None:
            self.books = BookController.get_all_books()
        else:
            book_filter = Filter(self.search_frame.list_combobox.get())
            self.books = BookController.get_books_by_filter(book_filter)
        self.populate_book_list()

    def populate_book_list(self):
        self.book_list.delete(*self.book_list.get_children())
        for book in self.books:
            self.book_list.insert(parent='', index=tk.END, values=(
                book.ISBN, book.title, book.author, book.pages, self.build_rating(book.rating)),
                                  tags=(self.listNotNone(book),))

    def listNotNone(self, book):
        if book.list is None:
            return "None"
        else:
            return book.list.name

    def build_rating(self, rating):
        if rating is None:
            return ""
        else:
            return "★" * rating + "☆" * (5 - rating)

    def find_all_lists(self):
        all_lists = ListController.get_all_lists()

        self.lists = ["None"]
        for item in all_lists:
            self.lists.append(item.name)

    def update_lists(self, event):
        self.find_all_lists()
        self.search_frame.update_lists(self.lists)
        self.list_frame.update_lists(self.lists)

    def open_add_book_dialog(self):
        AddBookDialog(self, self.lists)

    def open_book_right_click_menu(self, event):
        selected_item_id = self.book_list.identify_row(event.y)
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
