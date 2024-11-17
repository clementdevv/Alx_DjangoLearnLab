
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse  
from .models import Book
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class BookApiTests(APITestCase):

    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2020
        }
        self.book = Book.objects.create(**self.book_data)
        self.url_create = reverse('book-create')
        self.url_list = reverse('book-list')
        self.url_detail = reverse('book-detail', kwargs={'pk': self.book.id})
        self.url_update = reverse('book-update', kwargs={'pk': self.book.id})
        self.url_delete = reverse('book-delete', kwargs={'pk': self.book.id})

    def test_create_book_authenticated(self):
        # Test POST request to create a new book (authenticated)
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.url_create, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # One book already created in setUp

    def test_create_book_unauthenticated(self):
        # Test POST request to create a new book (unauthenticated)
        response = self.client.post(self.url_create, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_book_list(self):
        # Test GET request to retrieve the list of books
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # One book created in setUp

    def test_get_book_detail(self):
        # Test GET request to retrieve a book's detail
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book_authenticated(self):
        # Test PUT request to update an existing book (authenticated)
        updated_data = {
            'title': 'Updated Test Book',
            'author': 'Updated Author',
            'publication_year': 2021
        }
        self.client.login(username='testuser', password='password123')
        response = self.client.put(self.url_update, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Test Book')

    def test_update_book_unauthenticated(self):
        # Test PUT request to update a book (unauthenticated)
        updated_data = {
            'title': 'Updated Test Book',
            'author': 'Updated Author',
            'publication_year': 2021
        }
        response = self.client.put(self.url_update, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        # Test DELETE request to delete a book (authenticated)
        self.client.login(username='testuser', password='password123')
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_unauthenticated(self):
        # Test DELETE request to delete a book (unauthenticated)
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books_by_title(self):
        # Test GET request with filter query parameter (searching by title)
        response = self.client.get(self.url_list, {'title': 'Test Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_books_by_author(self):
        # Test GET request with filter query parameter (searching by author)
        response = self.client.get(self.url_list, {'author': 'Test Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_year(self):
        # Test GET request with ordering query parameter (ordering by publication year)
        response = self.client.get(self.url_list, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], self.book.publication_year)

    def test_search_books(self):
        # Test GET request with search query parameter (searching by title and author)
        response = self.client.get(self.url_list, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_permission_authenticated(self):
        # Test that permission class is enforced
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_unauthenticated(self):
        # Test that permission class restricts unauthenticated users
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
