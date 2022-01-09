import tkinter as tk
import tkinter.messagebox as msg_box
import logging
from Controllers import GoogleBooksApi, BookController, ListController

logger = logging.getLogger(__name__)


class AddBookDialog(tk.Toplevel):
    def __init__(self, parent, lists):
        super().__init__(parent)
        logger.debug("Initializing AddBookDialog")

        self.title("Add book")
        self.geometry("250x150")

        self.lists = lists

        self.isbn_label = tk.Label(self, text="ISBN:", font="Helvetica 16 bold")
        self.isbn_label.place(relx=0.1, rely=0.1, relheight=0.2, relwidth=0.3)

        self.isbn_entry = tk.Entry(self, font="Helvetica 12")
        self.isbn_entry.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.7)

        self.warning_label_text = tk.StringVar()
        self.warning_label_text.set("")
        self.warning_label = tk.Label(self, textvariable=self.warning_label_text, fg="red", font="Helvetica 8")
        self.warning_label.place(relx=0.1, rely=0.52, relheight=0.15, relwidth=0.7)

        self.list_combobox_option = tk.StringVar()
        self.list_combobox_option.set("None")

        # TODO: Replace with ttk.Combobox
        self.list_combobox = tk.OptionMenu(self, self.list_combobox_option, *self.lists)
        self.list_combobox.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.4)

        self.lookup_button = tk.Button(self, text="Add book", command=self.lookup)
        self.lookup_button.place(relx=0.6, rely=0.7, relheight=0.2, relwidth=0.3)

    def lookup(self):
        isbn = self.isbn_entry.get()
        # TODO: Add isbn validation. Otherwise books might still be added double.
        #  Since the api simply returns the nearest valid isbn
        # Check for alphabetical characters which are not allowed in an isbn
        if any(c.isalpha() for c in isbn):
            self.warning_label_text.set("Value can only contain numbers")
        else:
            self.warning_label_text.set("")

            # Check if book with isbn input was already added
            if BookController.book_exists(isbn):
                self.warning_label_text.set("Book with isbn already exists")
            else:
                result = GoogleBooksApi.fetch_book(isbn)
                if result is None:
                    logger.info(f"No match was found for isbn: {isbn}")
                    self.warning_label_text.set("No match was found")
                else:
                    json_result = result.json()

                    isbn = ""
                    for item in json_result['items'][0]['volumeInfo']['industryIdentifiers']:
                        if item['type'] == "ISBN_13":
                            isbn = item['identifier']
                    title = json_result['items'][0]['volumeInfo']['title']
                    author = json_result['items'][0]['volumeInfo']['authors'][0]
                    pages = json_result['items'][0]['volumeInfo']['pageCount']

                    insert_result = BookController.add_book(isbn, title, author, pages)
                    if insert_result is None:
                        ListController.move_book_to_list(isbn, self.list_combobox_option.get())
                        self.master.event_generate("<<BookUpdate>>")
                        self.destroy()
                    else:
                        msg_box.showerror("Error while inserting book", insert_result)
