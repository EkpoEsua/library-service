from rest_framework import generics
from books.serializers import BookBorrowSerializer, BookCreateSerializer, BookListSerializer
from books import filters
from books.models import Book

class BookListView(generics.ListAPIView):
    """List all books available in the catalogue, or depending on get query parameter."""
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [filters.PublisherFilter, filters.CategoryFilter]
    search_fields = ["publisher", "category"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(status="a")

class BookCreateView(generics.CreateAPIView):
    """Create a new book in the catalogue"""
    serializer_class = BookCreateSerializer

class BookDetailView(generics.RetrieveAPIView):
    """Detail view of a Book."""
    queryset = Book.objects.all()
    serializer_class = BookListSerializer

class BookBorrowView(generics.UpdateAPIView):
    """Borrow book from the catalogue supplying the register email of the user"""
    queryset = Book.objects.all()
    serializer_class = BookBorrowSerializer

    @property
    def allowed_methods(self):
        return ["PUT"]

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class BookDeleteView(generics.DestroyAPIView):
    """Delete book given by the book id"""
    queryset = Book.objects.all()


class BorrowedBooksListView(generics.ListAPIView):
    """List of borrowed books in the catalogue."""
    queryset = Book.objects.all()
    serializer_class = BookListSerializer

    def get_queryset(self):
        queryset =  super().get_queryset()
        return queryset.filter(status="b")
