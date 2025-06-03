from pydantic import BaseModel
from typing import List
import json
import os
from functools import wraps

# Модель книги
class BookModel(BaseModel):
    title: str
    author: str
    year: int

# Клас "Книга"
class Book:
    def __init__(self, book_model: BookModel):
        self._book_model = book_model

    def info(self) -> str:
        return f"{self._book_model.title} by {self._book_model.author}, published in {self._book_model.year}"

# Декоратор для логування
def log_addition(func):
    @wraps(func)
    def wrapper(self, book: Book):
        print(f"Adding book: {book.info()}")
        return func(self, book)
    return wrapper

def check_book_exists(func):
    @wraps(func)
    def wrapper(self, book: Book):
        if book in self.books:
            return func(self, book)
        print(f"Book not found: {book.info()}")
    return wrapper

# Клас "Бібліотека"
class Library:
    def __init__(self):
        self._books: List[Book] = []

    def __iter__(self):
        return iter(self._books)

    @log_addition
    def add_book(self, book: Book):
        self._books.append(book)

    @check_book_exists
    def remove_book(self, book: Book):
        self._books.remove(book)

    def find_books_by_author(self, author: str) -> List[Book]:
        return [book for book in self._books if book._book_model.author == author]

    @property
    def books(self) -> List[Book]:
        return self._books

    def book_generator(self, author: str):
        for book in self._books:
            if book._book_model.author == author:
                yield book

    def save_to_file(self, filename: str):
        with open(filename, 'w') as f:
            json.dump([book._book_model.dict() for book in self._books], f)

    def load_from_file(self, filename: str):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                books_data = json.load(f)
                for book_data in books_data:
                    self.add_book(Book(BookModel(**book_data)))

# Контекстний менеджер для роботи з файлами
class FileManager:
    def __init__(self, filename: str):
        self.filename = filename

    def __enter__(self):
        return self.filename

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Клас "Журнал", який наслідується від "Книги"
class Magazine(Book):
    def info(self) -> str:
        return f"Magazine: {self._book_model.title} by {self._book_model.author}, published in {self._book_model.year}"

# Використання класів
library = Library()

# Створення інстансів книги та журналу
book1 = Book(BookModel(title="1984", author="George Orwell", year=1949))
book2 = Book(BookModel(title="To Kill a Mockingbird", author="Harper Lee", year=1960))
magazine1 = Magazine(BookModel(title="National Geographic", author="Various", year=2021))

# Додавання книг до бібліотеки
library.add_book(book1)
library.add_book(book2)
library.add_book(magazine1)

# Виведення списку книг
print("Books in library:")
for book in library:
    print(book.info())

# Виведення книг за автором
author_books = library.find_books_by_author("George Orwell")
print("\nBooks by George Orwell:")
for book in author_books:
    print(book.info())

# Збереження книг у файл
library.save_to_file("library.json")

# Видалення книги з бібліотеки
library.remove_book(book1)
print("\nBooks in library after removal:")
for book in library:
    print(book.info())

# Додавання книг з файлу
library.load_from_file("library.json")
print("\nBooks in library after loading from file:")
for book in library:
    print(book.info())