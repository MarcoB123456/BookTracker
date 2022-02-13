import logging

import pandas as pd

from Controllers import GoogleBooksApi, BookTrackerUtils
from Models.Author import Author
from Models.Book import Book
from Models.List import List
from Models.Peewee import db
from Models.Read import Read

logger = logging.getLogger(__name__)


def fix_title(title):
    return title.split(" (")[0]


def fix_isbn(isbn):
    return isbn.replace("=\"", "").replace("\"", "")


def format_date(date):
    year, month, day = date.split("/")
    return f"{day}-{month}-{year}"


def combine_authors(author, additional_authors):
    if additional_authors != "":
        return f"{author}, {additional_authors}"
    else:
        return author


def combine_shelves(exclusiveShelf, bookShelf):
    if bookShelf == "No":
        return exclusiveShelf
    else:
        return bookShelf


def insert_lists(list_names):
    lists = {}
    for list_name in list_names:
        logger.debug(f"Attempting to get or create list with name: {list_name}")
        list_, created = List.get_or_create(name=list_name)
        lists[list_name] = list_.list_id

    return lists


def insert_authors(all_authors):
    authors = {}
    for author_entry in all_authors:
        for author in [author.strip() for author in author_entry.split(",")]:
            if author not in authors:
                logger.debug(f"Attempting to get or create author with name: {author}")
                new_author, created = Author.get_or_create(name=author)
                authors[author] = new_author.author_id

    return authors


def insert_book_and_readings_and_authors(book, lists, authors):
    # Fetch cover image

    if book['ISBN13'] != "":
        isbn = book['ISBN13']
    elif book["ISBN"] != "":
        isbn = book['ISBN']
    else:
        isbn = ""
        logger.debug(f"Found book without isbn with title: {book['Title']}")

    logger.debug(f"Attempting to insert book with isbn: {isbn} and title: {book['Title']}")

    cover_image = "Default.jpg"
    if isbn != "":
        result = GoogleBooksApi.fetch_book(book["ISBN13"])
        if result is not None:
            json_result = result.json()
            if "imageLinks" in json_result['items'][0]['volumeInfo']:
                cover_image = BookTrackerUtils.save_image(
                    json_result['items'][0]['volumeInfo']['imageLinks']['thumbnail'], isbn)

    new_book = Book.create(ISBN=isbn, title=book["Title"], pages=book["Pages"], rating=book["Rating"],
                           cover_image=cover_image, list=lists[book["List"]])
    # Add authors
    for author in [author.strip() for author in book["Authors"].split(",")]:
        new_book.authors.add(Author.get_by_id(authors[author]))

    # Add reading
    if book["List"] == "Finished":
        Read.create(start_date=book["Start_date"], end_date=book["End_date"], book_id=new_book.book_id)


def import_goodreads_file(url):
    df = pd.read_csv(url)

    df.drop(columns=['Book Id', 'Author l-f',
                     'Average Rating', 'Publisher', 'Binding',
                     'Year Published', 'Original Publication Year',
                     'Bookshelves with positions',
                     'My Review', 'Spoiler', 'Private Notes',
                     'Read Count', 'Recommended For', 'Recommended By', 'Owned Copies',
                     'Original Purchase Date', 'Original Purchase Location', 'Condition',
                     'Condition Description', 'BCID'], inplace=True)

    # Fill empty rows in Bookshelves column
    df["Bookshelves"] = df["Bookshelves"].fillna("No")

    # Combine both bookshelf columns into one List column
    df["List"] = df.apply(lambda x: combine_shelves(x['Exclusive Shelf'], x['Bookshelves']), axis=1)
    df.drop(columns=['Exclusive Shelf', 'Bookshelves'], inplace=True)

    # Combine author columns
    df["Additional Authors"] = df["Additional Authors"].fillna("")
    df["Authors"] = df.apply(lambda x: combine_authors(x['Author'], x['Additional Authors']), axis=1)
    df.drop(columns=['Author', 'Additional Authors'], inplace=True)

    # Replace Goodreads column names with mine:
    df.loc[df.List == "read", "List"] = 'Finished'
    df.loc[df.List == "to-read", "List"] = 'To-read'
    df.loc[df.List == "dropped", "List"] = 'Dropped'
    df.loc[df.List == "currently-reading", "List"] = 'Reading'

    # Remove Series indicator from the title value
    df["Title"] = df.apply(lambda x: fix_title(x['Title']), axis=1)

    # Rename columns
    df.rename(columns={'Number of Pages': 'Pages', 'My Rating': 'Rating', "Date Read": "End_date",
                       "Date Added": "Start_date"}, inplace=True)

    # Fix ISBN fields
    df["ISBN"] = df.apply(lambda x: fix_isbn(x['ISBN']), axis=1)
    df["ISBN13"] = df.apply(lambda x: fix_isbn(x['ISBN13']), axis=1)

    # Round Pages by turning it to int
    df.Pages = df.Pages.fillna(0)
    df['Pages'] = df['Pages'].astype(int)

    # Change date format
    df[['Start_date', 'End_date']] = df[['Start_date', 'End_date']].apply(pd.to_datetime)
    df.Start_date = df.Start_date.dt.strftime("%d-%m-%Y")
    df.End_date = df.End_date.dt.strftime("%d-%m-%Y")

    with db.atomic() as transaction:
        try:
            # Insert all lists
            lists = insert_lists(df["List"].unique())

            # Insert all authors
            authors = insert_authors(df["Authors"].unique())

            # Insert all books and readings
            for index, row in df.iterrows():
                insert_book_and_readings_and_authors(row, lists, authors)

        except Exception as exception:
            transaction.rollback()
            raise exception


if __name__ == '__main__':
    import_goodreads_file("goodreads_library_export.csv")
