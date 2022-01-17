import logging
import tkinter as tk

from Controllers import ListController

logger = logging.getLogger(__name__)


class AddListDialog(tk.Toplevel):
    def __init__(self, parent, lists, result):
        super().__init__(parent)
        self.lists = lists
        self.result = result

        logger.debug("Initializing AddListDialog")

        self.title("Add List")
        self.geometry("250x150")

        self.list_label = tk.Label(self, text="List name:", font="Helvetica 16 bold")
        self.list_label.place(relx=0.1, rely=0.1, relheight=0.2, relwidth=0.5)

        self.list_entry = tk.Entry(self, font="Helvetica 12")
        self.list_entry.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.7)

        self.warning_label_text = tk.StringVar()
        self.warning_label_text.set("")
        self.warning_label = tk.Label(self, textvariable=self.warning_label_text, fg="red", font="Helvetica 8")
        self.warning_label.place(relx=0.1, rely=0.52, relheight=0.15, relwidth=0.7)

        self.add_button = tk.Button(self, text="Add list", command=self.add_list)
        self.add_button.place(relx=0.6, rely=0.7, relheight=0.2, relwidth=0.3)

    def add_list(self):
        list_name = self.list_entry.get()
        # Check if list already exists
        if list_name in self.lists:
            self.warning_label_text.set("List already exists")
        else:
            result = ListController.add_list(list_name)
            if result is not None:
                self.result.set(list_name)
                self.destroy()
