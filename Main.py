from UI.Application import Application
import sqlite3
import logging


def log_init():
    logging.basicConfig(filename="main.log",
                        filemode="a",
                        format="%(asctime)s | %(levelname)s | %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.DEBUG)


def db_init():
    conn = sqlite3.connect("test.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS Book
                    (Id INTEGER NOT NULL PRIMARY KEY,
                    ISBN TEXT NOT NULL,
                    Title TEXT NOT NULL,
                    Author TEXT NOT NULL,
                    Pages TEXT,
                    Rating INTEGER,
                    ListId INTEGER,
                    FOREIGN KEY(ListId) REFERENCES List(ID));""")

    conn.execute("""CREATE TABLE IF NOT EXISTS List
                    (Id INTEGER NOT NULL PRIMARY KEY,
                    Name TEXT NOT NULL);""")

    # conn.execute("INSERT INTO List (Name) VALUES ('Reading')")
    # conn.execute("INSERT INTO List (Name) VALUES ('To-read')")
    # conn.execute("INSERT INTO List (Name) VALUES ('Dropped')")
    #
    # conn.execute("INSERT INTO Book (ISBN, Title, Author, Pages, ListId) VALUES ('123','Title A','Author A','123', 1)")
    # conn.execute("INSERT INTO Book (ISBN, Title, Author, Pages) VALUES ('456','Title B','Author B','233')")
    # conn.execute("INSERT INTO Book (ISBN, Title, Author, Pages) VALUES ('789','Title C','Author C','456')")

    conn.commit()
    conn.close()


if __name__ == '__main__':
    log_init()
    db_init()
    Application()
