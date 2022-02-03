import logging
import tkinter as tk
import tkinter.messagebox as msg_box

from Controllers import BookController

logger = logging.getLogger(__name__)


class BookRightClickMenu(tk.Menu):
    def __init__(self, parent, event, item, lists):
        super().__init__(parent, tearoff=0)

        self.item = item

        self.add_command(label="Copy isbn", command=lambda: self.copy_value(0))
        self.add_command(label="Copy title", command=lambda: self.copy_value(1))
        self.add_command(label="Copy author", command=lambda: self.copy_value(2))
        self.add_command(label="Copy pages", command=lambda: self.copy_value(3))
        self.add_command(label="Copy list", command=lambda: self.copy_value(4))
        self.add_separator()
        self.add_command(label="Delete book", command=self.delete_book)
        if self.item["tags"][0] != "None":
            self.add_command(label="Remove from list", command=self.remove_book_from_list)

        # Build list portion
        self.list_menu = tk.Menu(self)
        for list_item in lists.get():
            if list_item == self.item["tags"][0]:
                list_item = list_item + " ✓"
            self.list_menu.add_command(label=list_item,
                                       command=lambda list_item=list_item: self.move_book_to_list(list_item))
        self.add_cascade(label="Move to list", menu=self.list_menu)
        self.add_separator()

        # Build rating portion
        self.rating_menu = tk.Menu(self)
        self.rating_menu.add_command(label="★☆☆☆☆", command=lambda: self.update_rating(1))
        self.rating_menu.add_command(label="★★☆☆☆", command=lambda: self.update_rating(2))
        self.rating_menu.add_command(label="★★★☆☆", command=lambda: self.update_rating(3))
        self.rating_menu.add_command(label="★★★★☆", command=lambda: self.update_rating(4))
        self.rating_menu.add_command(label="★★★★★", command=lambda: self.update_rating(5))

        self.add_cascade(label="Rating", menu=self.rating_menu)

        self.tk_popup(event.x_root, event.y_root)

    def copy_value(self, value):
        logger.debug(f"Copying value with index {0} from selected item")
        self.clipboard_clear()
        if value == 4:
            self.clipboard_append(self.item['tags'][0])
        else:
            self.clipboard_append(self.item['values'][value])
        self.update()

    def delete_book(self):
        logger.debug("Started deletion process for a book")
        if msg_box.askyesno("Delete book", f"Are you sure you want to delete: {self.item['values'][1]}"):
            logger.debug(
                f"Confirmed deletion of book with isbn: {self.item['values'][0]}, title: {self.item['values'][1]}")
            BookController.remove_book(self.item['values'][0])
            self.master.event_generate("<<BookUpdate>>")
        else:
            logger.debug("Rejected deletion process")

    def move_book_to_list(self, list_name):
        # TODO: Add confirm window if already in a list. Not sure if this is actually needed
        BookController.move_book_to_list(self.item['values'][0], list_name)
        self.master.event_generate("<<BookUpdate>>")

    def remove_book_from_list(self):
        BookController.remove_book_from_list(self.item['values'][0])
        self.master.event_generate("<<BookUpdate>>")

    def update_rating(self, rating):
        BookController.update_book_rating(self.item['values'][0], rating)
        self.master.event_generate("<<BookUpdate>>")

