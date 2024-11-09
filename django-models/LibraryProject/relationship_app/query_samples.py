from relationship_app.models import Author, Book, Library, Librarian

def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name = author_name)        
        return author.books.all()
    except Author.DoesNotExist:
        return []
    
def list_library_books(library_name):
    try: 
        library = Library.objects.get(name = library_name)        
        return library.books.all()
    except Library.DoesNotExist:
        return []
    
def get_library_librarian(library_name):
    try: 
        library = Library.objects.get(name = library_name)
        return library.librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None