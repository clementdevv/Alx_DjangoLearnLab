from .views import (
    BookListView, 
    BookDetailView, 
    CustomBookCreateView, 
    CustomBookUpdateView, 
    BookDeleteView
)
from django.urls import path


urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  
    path('books/create/', CustomBookCreateView.as_view(), name='book-create'),  
    path('books/update/<int:pk>/', CustomBookUpdateView.as_view(), name='book-update'), 
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'), 

]