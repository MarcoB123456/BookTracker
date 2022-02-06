import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry

from UI.Custom.LabelInput import LabelInput


class AddBookDialogExtraFields(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.start_date_input_conf = {"relx": 0.1, "rely": 0.1, "relwidth": 0.35, "relheight": 0.25}
        self.end_date_input_conf = {"relx": 0.1, "rely": 0.5, "relwidth": 0.35, "relheight": 0.25}
        self.rating_input_conf = {"relx": 0.5, "rely": 0.1, "relwidth": 0.35, "relheight": 0.25}

        self.start_date_input = LabelInput(self, "Start date: ", tk.StringVar, DateEntry,
                                           label_args={"font": "Helvetica 16"},
                                           input_args={"width": "16", "locale": "nl"})
        self.start_date_input.place(self.start_date_input_conf)

        self.end_date_input = LabelInput(self, "Ending date: ", tk.StringVar, DateEntry,
                                         label_args={"font": "Helvetica 16"},
                                         input_args={"width": "16", "locale": "nl"})
        self.end_date_input.place(self.end_date_input_conf)

        self.rating_input_value = tk.StringVar()
        self.rating_input = LabelInput(self, "Rating:", self.rating_input_value, ttk.Combobox,
                                       label_args={"font": "Helvetica 16"},
                                       input_args={"values": ["", "★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★"]})
        self.rating_input.place(self.rating_input_conf)

    def show_fields(self, start_date=False, end_date=False, rating=False):
        if start_date:
            self.start_date_input.place_configure(self.start_date_input_conf)
        else:
            self.start_date_input.place_forget()

        if end_date:
            self.end_date_input.place_configure(self.end_date_input_conf)
        else:
            self.end_date_input.place_forget()

        if rating:
            self.rating_input.place_configure(self.rating_input_conf)
        else:
            self.rating_input.place_forget()

    def get_start_date(self, list_):
        if list_ == "Finished" or list_ == "Reading":
            return self.start_date_input.input.get_date().strftime('%d-%m-%Y')

    def get_end_date(self, list_):
        if list_ != "Finished":
            return None
        return self.end_date_input.input.get_date().strftime('%d-%m-%Y')

    def get_rating_index(self, list_):
        rating = self.rating_input.input.current()
        if rating == 0 or list_ == "Reading":
            return None
        return rating
