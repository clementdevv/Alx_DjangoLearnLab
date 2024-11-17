from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Book
from .forms import ExampleForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

