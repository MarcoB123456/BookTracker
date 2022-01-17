import tkinter as tk
from tkinter import messagebox as msg_box

from Controllers import BookController, ListController
from UI.AddListDialog import AddListDialog
from UI.UpdateListDialog import UpdateListDialog


class ListFrame(tk.Frame):
    def __init__(self, parent, lists):
        super().__init__(parent)
        # TODO: Add option to move books

        self.lists = lists

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

        self.populate_listbox()

    def populate_listbox(self):
        for item in self.lists:
            self.lists_list.insert(tk.END, item)

    def add_list(self):
        self.result = tk.StringVar()
        self.add_list_dialog = AddListDialog(self, self.lists, self.result)
        self.wait_window(self.add_list_dialog)
        if self.result.get() != "":
            self.lists.append(self.result.get())
            self.lists_list.insert(tk.END, self.result.get())
            self.master.event_generate("<<ListUpdate>>")

    def remove_list(self):
        cur_selection = self.lists_list.curselection()
        if len(cur_selection) != 0:
            list_name = self.lists_list.get(cur_selection)
            if msg_box.askyesno("Remove list", f"Are you sure you wish to delete list with name: {list_name}"):
                result = BookController.remove_all_books_from_list(list_name)
                if result is not None:
                    ListController.remove_list(list_name)

                self.lists_list.delete(cur_selection)
                self.lists.remove(list_name)
                self.master.event_generate("<<ListUpdate>>")
                self.master.event_generate("<<BookUpdate>>")

    def update_list(self):
        cur_selection = self.lists_list.curselection()
        if len(cur_selection) != 0:
            old_name = self.lists_list.get(cur_selection)

            self.update_list_result = tk.StringVar()
            self.update_list_dialog = UpdateListDialog(self, self.lists, old_name, self.update_list_result)
            self.wait_window(self.update_list_dialog)
            if self.update_list_result.get() != "":
                idx = self.lists.index(old_name)
                self.lists[idx] = self.update_list_result.get()
                self.lists_list.delete(cur_selection)
                self.lists_list.insert(tk.END, self.update_list_result.get())
                self.master.event_generate("<<ListUpdate>>")
                self.master.event_generate("<<BookUpdate>>")

    def update_lists(self, lists):
        self.lists = lists
        self.lists_list.delete(0, tk.END)
        for item in self.lists:
            self.lists_list.insert(tk.END, item)

    def show(self):
        self.tkraise()
