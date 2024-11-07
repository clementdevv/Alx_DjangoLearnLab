# Import the Book model from the bookshelf app
>>> from bookshelf.models import Book

# Retrieve the book with the title "1984" (or any other method of querying)
>>> book = Book.objects.get(title="1984")
>>> book

# Expected output:
# <Book: 1984>

# Display all attributes of the retrieved book
>>> book.title
# Expected output:
# '1984'

>>> book.author
# Expected output:
# 'George Orwell'

>>> book.publication_year
# Expected output:
# 1949
