import tkinter as tk

from Controllers import ListFrameController
from UI.Custom.JSONVar import JSONVar
from UI.Dialogs.AddListDialog import AddListDialog
from UI.Dialogs.UpdateListDialog import UpdateListDialog


class ListFrame(tk.Frame):
    controller = ListFrameController

    def __init__(self, parent, lists: JSONVar):
        super().__init__(parent)
        # TODO: Add option to move books

        self.lists = lists
        self.lists.trace_add('write', self._populate_listbox)

        self.title_label = tk.Label(self, text="Lists", font="Helvetica 18 bold")
        self.title_label.place(relx=0, rely=0.05, relheight=0.1, relwidth=1)

        self.lists_list = tk.Listbox(self, selectbackground="gray")
        self.lists_list.place(relx=0.1, rely=0.18, relheight=0.7, relwidth=0.8)

        self.button_width = 0.8 / 3
        self.add_button = tk.Button(self, text="+", font="Helvetica 16", command=self.add_list)
        self.add_button.place(relx=0.1, rely=0.88, relheight=0.1, relwidth=self.button_width)

        self.update_button = tk.Button(self, text="✎", font="Helvetica 16", command=self.update_list)
        self.update_button.place(relx=0.1 + self.button_width, rely=0.88, relheight=0.1, relwidth=self.button_width)

        self.remove_button = tk.Button(self, text="-", font="Helvetica 16", command=self.remove_list)
        self.remove_button.place(relx=0.1 + (self.button_width * 2), rely=0.88, relheight=0.1,
                                 relwidth=self.button_width)

        self._populate_listbox()

    def _populate_listbox(self, *_):
        self.lists_list.delete(0, tk.END)
        for item in self.lists.get():
            self.lists_list.insert(tk.END, item)

    def add_list(self):
        result = tk.StringVar()
        add_list_dialog = AddListDialog(self, self.lists, result)
        self.wait_window(add_list_dialog)
        if result.get() != "":
            curr_list = self.lists.get()
            curr_list.append(result.get())
            self.lists.set(curr_list)

    def remove_list(self):
        cur_selection = self.lists_list.curselection()
        if cur_selection:
            list_name = self.lists_list.get(cur_selection)
            removed_rows = self.controller.remove_list(list_name)
            if removed_rows:
                curr_list = self.lists.get()
                curr_list.remove(list_name)
                self.lists.set(curr_list)
                self.master.event_generate("<<PaginationUpdate>>")

    def update_list(self):
        cur_selection = self.lists_list.curselection()
        if cur_selection:
            old_name = self.lists_list.get(cur_selection)

            # Open dialog
            update_list_result = tk.StringVar()
            update_list_dialog = UpdateListDialog(self, self.lists, old_name, update_list_result)
            self.wait_window(update_list_dialog)
            if update_list_result.get() != "":
                idx = self.lists.get().index(old_name)
                old_list = self.lists.get()
                old_list[idx] = update_list_result.get()
                self.lists.set(old_list)
                self.master.event_generate("<<PaginationUpdate>>")

    def show(self):
        self.tkraise()
