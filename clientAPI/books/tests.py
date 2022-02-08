from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User
from rest_framework import status
from books.models import Book
from django.utils import timezone


class ClientAPITestCase(APITestCase):
    def setUp(self) -> None:
        """Setup data for test methods."""
        # Create books in the database
        Book.objects.create(
            title="Just One Bite", publisher="Jay Lender", category="comedy"
        )
        Book.objects.create(
            title="Jellyfish Jam", publisher="Ennio", category="horror", status="b"
        )
        Book.objects.create(
            title="Sandy's Rocket", publisher="Cohen", category="science"
        )
        Book.objects.create(
            title="Mermaid Man and Barnacle Boy", publisher="Cohen", category="science"
        )

        # Create user in database
        User.objects.create(
            email="squidward.t@kk.com", first_name="Squidward", last_name="Tentacles"
        )

    def test_get_list_of_all_available_books(self):
        """Get a list of books whose status is available in the library."""
        url = reverse("book-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)

    def test_for_getting_a_book_from_the_library_by_id(self):
        """Get a book in the library by id."""
        url = reverse("book-detail", kwargs={"pk": 2})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = {
            "id": 2,
            "title": "Jellyfish Jam",
            "status": "b",
            "publisher": "Ennio",
            "category": "horror",
            "due_back": None,
            "borrow_duration": None,
            "borrower": None,
        }
        self.assertEqual(response.data, response_data)

    def test_filter_books_by_publisher(self):
        """Filter the list of books in the library by publisher field."""
        url: str = reverse("book-list")
        url = url + "?publisher=Cohen"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_filter_books_by_category(self):
        """Filter the list of books in the library by category field."""
        url: str = reverse("book-list")
        url = url + "?category=science"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_borrow_book_by_id(self):
        """Test user Borrowing book by id."""
        book: Book = Book.objects.get(pk=1)
        self.assertEqual(book.status, "a")
        url = reverse("borrow-book", kwargs={"pk": 1})
        data = {
            "borrow_duration": 5,
            "borrower": "squidward.t@kk.com"}
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowed_book: Book = Book.objects.get(pk=1)
        self.assertEqual(borrowed_book.status, "b")
        self.assertEqual(borrowed_book.borrow_duration, 5)
        self.assertEqual(borrowed_book.due_back, timezone.now().date() + timezone.timedelta(days=5))
