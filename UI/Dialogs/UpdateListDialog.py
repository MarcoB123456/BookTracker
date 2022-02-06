import logging
import tkinter as tk

from Controllers import UpdateListDialogController

logger = logging.getLogger(__name__)


class UpdateListDialog(tk.Toplevel):
    controller = UpdateListDialogController

    def __init__(self, parent, lists, old_name, result):
        super().__init__(parent)
        self.lists = lists
        self.old_name = old_name
        self.result = result

        logger.debug("Initializing UpdateListDialog")

        self.title("Update List")
        self.geometry("250x150")

        self.list_label = tk.Label(self, text="New name:", font="Helvetica 16 bold")
        self.list_label.place(relx=0.1, rely=0.1, relheight=0.2, relwidth=0.5)

        self.list_entry = tk.Entry(self, font="Helvetica 12")
        self.list_entry.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.7)

        self.warning_label_text = tk.StringVar()
        self.warning_label_text.set("")
        self.warning_label = tk.Label(self, textvariable=self.warning_label_text, fg="red", font="Helvetica 8")
        self.warning_label.place(relx=0.1, rely=0.52, relheight=0.15, relwidth=0.7)

        self.update_button = tk.Button(self, text="Update list", command=self.update_list)
        self.update_button.place(relx=0.6, rely=0.7, relheight=0.2, relwidth=0.3)

    def update_list(self):
        new_name = self.list_entry.get()
        # Check if list already exists
        if new_name == self.old_name:
            self.warning_label_text.set("Name cannot be the same")
        elif new_name in self.lists.get():
            self.warning_label_text.set("List already exists")
        else:
            result = self.controller.update_list(new_name, self.old_name)
            if result is not None:
                self.result.set(new_name)
                self.destroy()
