import tkinter as tk
from tkinter import ttk


class SearchFrame(tk.Frame):
    def __init__(self, parent, lists):
        super().__init__(parent)

        self.bind()

        self.lists = lists

        # Build list filter
        self.list_label = tk.Label(self, text="List", anchor=tk.W, font="Helvetica 14 bold")
        self.list_label.place(relx=0.1, rely=0.03, relwidth=0.8, relheight=0.05)

        self.list_combobox_selected = tk.StringVar()
        self.list_combobox = ttk.Combobox(self)
        self.list_combobox.bind('<<ComboboxSelected>>', self.list_filter_changed)

        self.list_combobox["values"] = self.lists
        self.list_combobox.set('None')
        self.list_combobox.place(relx=0.1, rely=0.08, relwidth=0.80, relheight=0.07)

    def show(self):
        self.tkraise()

    def update_lists(self, lists):
        self.lists = lists
        self.list_combobox["values"] = self.lists

    def list_filter_changed(self, event):
        self.master.event_generate("<<BookUpdate>>")
