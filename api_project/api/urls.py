from django.db import router
from django.urls import include, path
from .views import BookList, BookViewSet

# router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('books/', BookList.as_view(), name='book-list'),  
    path('get-token/', obtain_auth_token, name='api_token_auth'),

]