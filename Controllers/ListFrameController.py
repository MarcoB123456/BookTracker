from tkinter import messagebox as msg_box

from Service import BookService, ListService


def remove_list(list_name):
    if msg_box.askyesno("Remove list", f"Are you sure you wish to delete list with name: {list_name}"):
        BookService.remove_all_books_from_list(list_name)
        removed_rows = ListService.remove_list(list_name)
        if removed_rows:
            return removed_rows
        else:
            msg_box.showerror("Warning while removing list", "List could not be removed")
