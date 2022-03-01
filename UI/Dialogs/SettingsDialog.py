import logging
import tkinter as tk
from tkinter import filedialog

from Definitions import VERSION
from Importers import GoodreadsImporter

logger = logging.getLogger(__name__)


class SettingsDialog(tk.Toplevel):
    height = 250
    width = 500

    def __init__(self, parent):
        super().__init__(parent)
        logger.debug("Initializing SettingsDialog")

        self.title("Settings")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(width=False, height=False)

        self.import_label = tk.Label(self, text="Import", font="Helvetica 16 bold underline")
        self.import_label.place(relx=0.1, rely=0.05, relheight=0.1, relwidth=0.3)

        self.import_goodreads_button = tk.Button(self, text="Goodreads", command=self.import_goodreads)
        self.import_goodreads_button.place(relx=0.1, rely=0.2, relheight=0.1, relwidth=0.3)

        # Version label
        self.version_label = tk.Label(self, text=f"V{VERSION}", fg="gray", justify=tk.LEFT)
        self.version_label.place(relx=0, rely=0.9, relheight=0.1, relwidth=0.1)

    @staticmethod
    def import_goodreads():
        src_path = filedialog.askopenfilename(filetypes=(("Csv file", "*.csv"), ("All files", "*.*")))
        GoodreadsImporter.import_goodreads_file(src_path)
