import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry


class LabelInput(tk.Frame):

    def __init__(self, parent, label_text, var, input_class=ttk.Entry, input_args=None, label_args=None, *args,
                 **kwargs):
        super().__init__(parent, *args, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = var
        self.variable.label_widget = self

        if input_class in (ttk.Checkbutton, ttk.Button):
            input_args["text"] = label_text
        else:
            self.label = ttk.Label(self, text=label_text, **label_args)
            self.label.place(relx=0, rely=0, relwidth=1, relheight=0.5)

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["variable"] = self.variable
        elif input_class != DateEntry:
            input_args["textvariable"] = self.variable

        if input_class == ttk.Radiobutton:
            self.input = tk.Frame(self)
            for v in input_args.pop('values', []):
                self.button = ttk.Radiobutton(self.input, value=v, text=v, **input_args)
                self.button.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
        else:
            self.input = input_class(self, **input_args)
            self.input.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

    def get_entry(self):
        return self.input.get()
