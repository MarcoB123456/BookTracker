import tkinter as tk
from tkinter import ttk

from Controllers import BookController, ListController
from UI.AddBookDialog import AddBookDialog
from UI.RightClickMenu import RightClickMenu


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tk.call("source", "sun-valley.tcl")
        self.tk.call("set_theme", "dark")
        self.title("BookTracker")
        self.geometry("1000x500")

        # Custom event's
        self.bind("<<BookUpdate>>", self.on_startup_populate_book_list)

        # Variables
        self.books = []
        self.lists = ["None"]

        # Build list filter
        self.list_label = tk.Label(self, text="List", anchor=tk.W, font="Helvetica 14 bold")
        self.list_label.place(relx=0.01, rely=0.03, relwidth=0.2, relheight=0.05)

        self.list_combobox_selected = tk.StringVar()
        self.list_combobox = ttk.Combobox(self)
        self.on_startup_populate_list_combobox()
        self.list_combobox.bind('<<ComboboxSelected>>', self.list_filter_changed)
        self.list_combobox.set('None')
        self.list_combobox.place(relx=0.01, rely=0.08, relwidth=0.18, relheight=0.07)

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
        self.book_list.bind("<Button-3>", self.open_right_click_menu)

        self.on_startup_populate_book_list()

        self.book_list.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)

        # Build add button
        self.add_book_button = tk.Button(self, text="+", font="Helvetica 20 bold", command=self.add_book)
        self.add_book_button.place(relx=0.1, rely=0.8, relheight=0.07, relwidth=0.07)
        self.mainloop()

    def on_startup_populate_book_list(self, event=None):
        self.books = BookController.get_all_books()
        self.insert_book_list_items()

    def insert_book_list_items(self):
        self.book_list.delete(*self.book_list.get_children())
        for book in self.books:
            self.book_list.insert(parent='', index=tk.END, values=(
                book.ISBN, book.title, book.author, book.pages, self.build_rating(book.rating)),
                                  tags=(book.list.name,))

    def build_rating(self, rating):
        if rating is None:
            return ""
        else:
            return "★" * rating + "☆" * (5 - rating)

    def on_startup_populate_list_combobox(self):
        result = ListController.get_all_lists()
        for list in result:
            self.lists.append(list.name)
        self.list_combobox['values'] = self.lists

    def list_filter_changed(self, event):
        if self.list_combobox.get() == "None":
            self.books = BookController.get_all_books()
        else:
            self.books = BookController.get_books_by_list(self.list_combobox.get())

        self.insert_book_list_items()

    def add_book(self):
        add_book_dialog = AddBookDialog(self)
        self.wait_window(add_book_dialog)
        self.on_startup_populate_book_list()

    def open_right_click_menu(self, event):
        selected_item_id = self.book_list.identify_row(event.y)
        self.book_list.selection_set(selected_item_id)
        selected_item = self.book_list.item(selected_item_id)
        RightClickMenu(self, event, selected_item, self.lists)

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: \
            self.treeview_sort_column(tv, col, not reverse))
