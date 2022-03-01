import logging
import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image
from tkcalendar import DateEntry

from Controllers import UpdateBookDialogController
from Controllers.BookTrackerUtils import build_rating, is_not_none
from Definitions import ROOT_PATH
from Models.Book import Book
from UI.Custom.LabelInput import LabelInput

logger = logging.getLogger(__name__)


class UpdateBookDialog(tk.Toplevel):
    height = 800
    width = 600
    controller = UpdateBookDialogController

    def __init__(self, parent, isbn, title, lists):
        super().__init__(parent)
        logger.debug("Initializing UpdateBookDialog")

        self.title("Update book")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(width=False, height=False)

        self.book: Book = self.controller.get_book(isbn, title)
        self.lists = lists

        # Cover image
        self._load_cover_image()
        self.image_label = tk.Label(self, image=self.img)
        self.image_label.place(relx=0.20, rely=0.22, relheight=0.4, relwidth=0.35, anchor=tk.CENTER)

        self.image_button = tk.Button(self, text="⤒", command=self._upload_cover_file)
        self.image_button.place_configure(relx=0.325, rely=0.38, relheight=0.04, relwidth=0.05)

        # ISBN
        self.isbn_input_value = tk.StringVar()
        self.isbn_input = LabelInput(self, "ISBN:", self.isbn_input_value)
        self.isbn_input.place(relx=0.40, rely=0.02, relheight=0.1, relwidth=0.5)

        # Title
        self.title_input_value = tk.StringVar()
        self.title_input = LabelInput(self, "Title:", self.title_input_value)
        self.title_input.place(relx=0.40, rely=0.12, relheight=0.1, relwidth=0.5)

        # Pages
        self.pages_input_value = tk.StringVar()
        self.pages_input = LabelInput(self, "Pages:", self.pages_input_value)
        self.pages_input.place(relx=0.4, rely=0.22, relheight=0.1, relwidth=0.15)

        # List
        self.list_input_value = tk.StringVar()
        self.list_input = LabelInput(self, "List:", self.list_input_value, ttk.Combobox,
                                     input_args={"values": self.lists.get()})
        self.list_input.place(relx=0.6, rely=0.22, relheight=0.1, relwidth=0.30)

        # Rating
        self.rating_input_value = tk.StringVar()
        self.rating_input = LabelInput(self, "Rating:", self.rating_input_value, ttk.Combobox,
                                       input_args={"values": ["", "★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★"]})
        self.rating_input.place(relx=0.40, rely=0.32, relheight=0.1, relwidth=0.20)

        # Reading
        self.reading_list_label = tk.Label(self, text="Readings:", justify=tk.LEFT)
        self.reading_list_label.place(relx=0.03, rely=0.43, relheight=0.05, relwidth=0.11)

        self.reading_list = tk.Listbox(self, selectbackground="gray")
        self.reading_list.place(relx=0.03, rely=0.48, relheight=0.4, relwidth=0.35)
        self.reading_list.bind('<<ListboxSelect>>', self._on_reading_select)

        self.reading_start_date_entry = DateEntry(self, width=16, locale="nl")
        self.reading_start_date_entry.place(relx=0.03, rely=0.88, relheight=0.05, relwidth=0.175)
        self.reading_start_date_entry.bind("<<DateEntrySelected>>", self._on_start_date_select)

        self.reading_end_date_entry = DateEntry(self, width=16, locale="nl")
        self.reading_end_date_entry.place(relx=0.205, rely=0.88, relheight=0.05, relwidth=0.175)

        self.add_reading_button = ttk.Button(self, text="Add", command=self._add_reading)
        self.add_reading_button.place(relx=0.03, rely=0.93, relheight=0.04, relwidth=0.11)

        self.update_reading_button = ttk.Button(self, text="Update", command=self._update_reading)
        self.update_reading_button.place(relx=0.14, rely=0.93, relheight=0.04, relwidth=0.12)

        self.remove_reading_button = ttk.Button(self, text="Remove", command=self._remove_reading)
        self.remove_reading_button.place(relx=0.26, rely=0.93, relheight=0.04, relwidth=0.12)

        # Author
        self.author_list_label = tk.Label(self, text="Authors:", justify=tk.LEFT)
        self.author_list_label.place(relx=0.40, rely=0.43, relheight=0.05, relwidth=0.11)

        self.author_list = tk.Listbox(self, selectbackground="gray")
        self.author_list.place(relx=0.40, rely=0.48, relheight=0.3, relwidth=0.35)
        self.author_list.bind('<<ListboxSelect>>', self._on_author_select)

        self.author_entry_value = tk.StringVar()
        self.author_start_entry = ttk.Entry(self, textvariable=self.author_entry_value)
        self.author_start_entry.place(relx=0.40, rely=0.78, relheight=0.05, relwidth=0.35)

        self.add_author_button = ttk.Button(self, text="Add", command=self._add_author)
        self.add_author_button.place(relx=0.40, rely=0.83, relheight=0.04, relwidth=0.11)

        self.update_author_button = ttk.Button(self, text="Update", command=self._update_author)
        self.update_author_button.place(relx=0.51, rely=0.83, relheight=0.04, relwidth=0.12)

        self.remove_author_button = ttk.Button(self, text="Remove", command=self._remove_author)
        self.remove_author_button.place(relx=0.63, rely=0.83, relheight=0.04, relwidth=0.12)

        # Save button
        self.save_button = tk.Button(self, text="Save", command=self._save_book)
        self.save_button.place(relx=0.83, rely=0.92, relheight=0.06, relwidth=0.15)

        # Cancel button
        self.cancel_button = tk.Button(self, text="Cancel", command=self._cancel_update)
        self.cancel_button.place(relx=0.66, rely=0.92, relheight=0.06, relwidth=0.15)

        self._fill_fields()

    def _add_author(self):
        self.author_list.insert(tk.END, self.author_entry_value.get())

    def _update_author(self):
        idx = self.author_list.curselection()
        if idx:
            self.author_list.delete(idx)
            self.author_list.insert(idx, self.author_entry_value.get())

    def _remove_author(self):
        idx = self.author_list.curselection()
        if idx:
            self.author_list.delete(idx)

    def _on_author_select(self, *_):
        idx = self.author_list.curselection()
        if idx:
            item = self.author_list.get(idx)
            self.author_entry_value.set(item)

    def _add_reading(self):
        self.reading_list.insert(tk.END,
                                 f"{self.reading_start_date_entry.get_date().strftime('%d-%m-%Y')} - {self.reading_end_date_entry.get_date().strftime('%d-%m-%Y')}")

    def _update_reading(self):
        idx = self.reading_list.curselection()
        if idx:
            self.reading_list.delete(idx)
            self.reading_list.insert(idx,
                                     f"{self.reading_start_date_entry.get_date().strftime('%d-%m-%Y')} - {self.reading_end_date_entry.get_date().strftime('%d-%m-%Y')}")

    def _remove_reading(self):
        idx = self.reading_list.curselection()
        if idx:
            self.reading_list.delete(idx)

    def _on_start_date_select(self, *_):
        if self.reading_end_date_entry.get_date() <= self.reading_start_date_entry.get_date():
            self.reading_end_date_entry.set_date(self.reading_start_date_entry.get_date())

    def _on_reading_select(self, *_):
        idx = self.reading_list.curselection()
        if idx:
            item = self.reading_list.get(idx)
            start_date, end_date = item.split(" - ")

            self.reading_start_date_entry.set_date(start_date)
            if is_not_none(end_date):
                self.reading_end_date_entry.set_date(end_date)

    def _save_book(self):
        isbn = self.isbn_input_value.get()
        title = self.title_input_value.get()
        pages = self.pages_input_value.get()
        rating = self.rating_input.input.current()
        list_name = self.list_input_value.get()
        reading_list = self.reading_list.get(0, tk.END)
        author_list = self.author_list.get(0, tk.END)

        updated_rows = self.controller.save_book(self.book.book_id, isbn, title, author_list, pages, rating, list_name,
                                                 reading_list)

        if updated_rows is not None:
            self.destroy()

    def _cancel_update(self):
        self.destroy()

    def _fill_fields(self):
        self.isbn_input_value.set(self.book.ISBN)
        self.title_input_value.set(self.book.title)
        self.pages_input_value.set(self.book.pages)
        self.rating_input_value.set(build_rating(self.book.rating))
        if self.book.list is not None:
            self.list_input_value.set(self.book.list.name)
        else:
            self.list_input_value.set("None")

        for read in self.book.get_readings():
            self.reading_list.insert(tk.END, f"{read.start_date} - {read.end_date}")

        for author in self.book.get_authors():
            self.author_list.insert(tk.END, author.name)

    def _load_cover_image(self):
        self.original_img = Image.open(f"{ROOT_PATH}\\Images\\Covers\\{self.book.cover_image}")
        self.resized_img = self.original_img.resize((int(self.width * 0.35), int(self.height * 0.4)), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.resized_img)

    def _upload_cover_file(self):
        self.book.cover_image = self.controller.upload_cover_image()
        self._load_cover_image()
        self.image_label.configure(image=self.img)
