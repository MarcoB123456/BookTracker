import logging
import tkinter as tk
from tkinter import ttk

from Controllers import AddBookDialogController
from UI.Custom.LabelInput import LabelInput
from UI.Dialogs.AddBookDialogExtraFields import AddBookDialogExtraFields

logger = logging.getLogger(__name__)


class AddBookDialog(tk.Toplevel):
    height = 250
    width = 500
    controller = AddBookDialogController

    def __init__(self, parent, lists, result_book):
        super().__init__(parent)
        logger.debug("Initializing AddBookDialog")

        self.title("Add book")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(width=False, height=False)

        self.lists = lists

        self.result_book = result_book

        self.main_frame = tk.Frame(self)
        self.main_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.isbn_input_value = tk.StringVar()
        self.isbn_input = LabelInput(self.main_frame, "ISBN:", self.isbn_input_value, ttk.Entry,
                                     label_args={"font": "Helvetica 16 bold"})
        self.isbn_input.place(relx=0.1, rely=0.1, relheight=0.4, relwidth=0.7)

        self.warning_label_text = tk.StringVar()
        self.warning_label_text.set("")
        self.warning_label = tk.Label(self.main_frame, textvariable=self.warning_label_text, fg="red",
                                      font="Helvetica 8", justify=tk.LEFT)
        self.warning_label.place(relx=0.1, rely=0.52, relheight=0.15, relwidth=0.7)

        self.list_combobox_option = tk.StringVar()
        self.list_combobox_option.set("None")

        self.list_combobox = ttk.Combobox(self.main_frame, textvariable=self.list_combobox_option)
        self.list_combobox.bind('<<ComboboxSelected>>', self.list_changed)
        self.list_combobox["values"] = self.lists.get()
        self.list_combobox.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.4)

        self.lookup_button = tk.Button(self.main_frame, text="Add book", command=self.lookup)
        self.lookup_button.place(relx=0.6, rely=0.7, relheight=0.2, relwidth=0.3)

        self.extra_options_frame = AddBookDialogExtraFields(self)

    def list_changed(self, *_):
        list_value = self.list_combobox_option.get()
        match list_value:
            case "Finished" | "Reading":
                self.geometry(f"{self.width * 2}x{self.height}")
                self.main_frame.place_configure(relwidth=0.5)
                self.extra_options_frame.place_configure(relx=0.5, rely=0, relheight=1, relwidth=0.5)
                if list_value == "Finished":
                    self.extra_options_frame.show_fields(True, True, True)
                else:
                    self.extra_options_frame.show_fields(start_date=True)
            case _:
                self.geometry(f"{self.width}x{self.height}")
                self.extra_options_frame.place_forget()
                self.main_frame.place_configure(relwidth=1)

    def lookup(self):
        isbn = self.isbn_input_value.get()
        list_ = self.list_combobox_option.get()
        rating = self.extra_options_frame.get_rating_index(list_)
        start_date = self.extra_options_frame.get_start_date(list_)
        end_date = self.extra_options_frame.get_end_date(list_)

        new_book = self.controller.add_book(isbn, list_, rating, start_date, end_date, self.warning_label_text)

        if new_book is not None:
            self.result_book.set(new_book.to_dict())
            self.destroy()
