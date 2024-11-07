# Import the Book model from the bookshelf app
>>> from bookshelf.models import Book

# Retrieve the book instance to delete
>>> book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book instance
>>> book.delete()

# Expected output:
# (1, {'bookshelf.Book': 1})  # This output confirms that one Book record was deleted

# Verify the deletion by attempting to retrieve the book again
>>> Book.objects.filter(title="Nineteen Eighty-Four")
# Expected output:
# <QuerySet []>  # An empty QuerySet indicates the book was successfully deleted
