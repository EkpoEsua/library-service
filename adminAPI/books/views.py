from rest_framework import generics
from books.serializers import (
    BookBorrowSerializer,
    BookCreateSerializer,
    BookListSerializer,
)
from books import filters
from books.models import Book
from source import emit_command


class BookListView(generics.ListAPIView):
    """List all books in the catalogue, depending on get query parameter."""

    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [filters.PublisherFilter, filters.CategoryFilter]
    search_fields = ["publisher", "category"]


class BookCreateView(generics.CreateAPIView):
    """Create a new book in the catalogue"""

    serializer_class = BookCreateSerializer


class BookDetailView(generics.RetrieveAPIView):
    """Detail view of a Book."""

    queryset = Book.objects.all()
    serializer_class = BookListSerializer


class BookUpdateView(generics.UpdateAPIView):
    """Borrow book from the catalogue"""

    queryset = Book.objects.all()
    serializer_class = BookBorrowSerializer


class BookDeleteView(generics.DestroyAPIView):
    """Delete book given by the book id"""

    queryset = Book.objects.all()

    def perform_destroy(self, instance):
        id = instance.pk
        super().perform_destroy(instance)
        emit_command(str(id), "clientapi.delete_book")


class BorrowedBooksListView(generics.ListAPIView):
    """List the books that are not available for borrowing (showing the day it will be available)"""

    queryset = Book.objects.all()
    serializer_class = BookListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(status="b")
