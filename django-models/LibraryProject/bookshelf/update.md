# Import the Book model from the bookshelf app
>>> from bookshelf.models import Book

# Retrieve the book instance to update
>>> book = Book.objects.get(title="1984")

# Update the title to "Nineteen Eighty-Four" and save the changes
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()

# Expected output after saving (re-querying to confirm the update):
>>> updated_book = Book.objects.get(id=book.id)
>>> updated_book.title
# Expected output:
# 'Nineteen Eighty-Four'
