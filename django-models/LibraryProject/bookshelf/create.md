# Import the Book model from the bookshelf app
>>> from bookshelf.models import Book

# Create a new Book instance with the title "1984", author "George Orwell", and publication year 1949
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Expected output:
# <Book: 1984>
