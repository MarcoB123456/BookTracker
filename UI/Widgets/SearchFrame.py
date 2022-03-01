import tkinter as tk
from tkinter import ttk

from Models.Filter import Filter
from UI.Custom.JSONVar import JSONVar
from UI.Custom.LabelInput import LabelInput


class SearchFrame(tk.Frame):
    def __init__(self, parent, lists: JSONVar):
        super().__init__(parent)

        self.bind()

        self.lists = lists
        self.lists.trace_add('write', self._update_lists)

        # List filter
        self.list_input_value = tk.StringVar()
        self.list_input_value.set("None")
        self.list_input = LabelInput(self, "List:", self.list_input_value, ttk.Combobox,
                                     label_args={"font": "Helvetica 14 bold"},
                                     input_args={"values": self.lists.get()})
        self.list_input.place(relx=0.1, rely=0.03, relwidth=0.8, relheight=0.12)
        self.list_input.input.bind('<<ComboboxSelected>>', self.list_filter_changed)

    def show(self):
        self.tkraise()

    def _update_lists(self, *_):
        self.list_input.input["values"] = self.lists.get()

    def get_filter(self):
        return Filter(self.list_input_value.get())

    def list_filter_changed(self, *_):
        self.master.event_generate("<<ListFilterUpdate>>")
