from rest_framework import generics, filters
from .models import Book 
from.serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework 
# import DjangoFilterBackend

class CustomBookCreateView(generics.CreateAPIView):    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):                
        publication_year = request.data.get('publication_year')        
        try:
            publication_year = int(publication_year)         
            if publication_year < 1800:
                return Response(
                    {"error": "Publication year cannot be before 1800"},
                    status=status.HTTP_400_BAD_REQUEST
                )            
            if publication_year > 2024:
                return Response(
                    {"error": "Publication year cannot be in the future"},
                    status=status.HTTP_400_BAD_REQUEST
                )        
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid publication year"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Perform standard create operation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)    
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

class CustomBookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    def partial_update(self, request, *args, **kwargs):        
        # Retrieve the existing book instance
        instance = self.get_object()
        
        # Custom update constraints
        # Prevent updating books published before 2000
        if instance.publication_year < 2000:
            return Response(
                {"error": "Cannot update books published before 2000"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validate publication year if provided
        publication_year = request.data.get('publication_year')
        if publication_year:
            try:
                publication_year = int(publication_year)
                if publication_year > 2024:
                    return Response(
                        {"error": "Publication year cannot be in the future"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except (ValueError, TypeError):
                return Response(
                    {"error": "Invalid publication year"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Perform standard partial update
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)



class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['title', 'author', 'publication_year']  
    ordering_fields = ['publication_year', 'title']  
    ordering = ['publication_year']  

    
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
# class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
    