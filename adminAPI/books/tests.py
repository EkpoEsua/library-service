from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User
from rest_framework import status
from books.models import Book
from django.utils import timezone


class AdminAPITestCase(APITestCase):
    def setUp(self) -> None:
        """Setup data for test methods."""
        # Create books in the database
        book1: Book = Book.objects.create(
            title="Just One Bite", publisher="Jay Lender", category="comedy"
        )
        book2: Book = Book.objects.create(
            title="Jellyfish Jam", publisher="Ennio", category="horror"
        )
        book3: Book = Book.objects.create(
            title="Sandy's Rocket", publisher="Cohen", category="science"
        )

        # Create user in database
        squidy = User.objects.create(
            email="squidward.t@kk.com", first_name="Squidward", last_name="Tentacles"
        )

        # Borrow some books
        book1.borrower = squidy
        book1.status = "b"
        book1.borrow_duration = 5
        book1.save()
        book2.borrower = squidy
        book2.status = "b"
        book2.borrow_duration = 10
        book2.save()

    def test_adding_a_new_book(self):
        """Test adding a new book to the library."""
        self.assertEqual(Book.objects.count(), 3)
        url = reverse("create-book")
        data = {
            "title": "Mermaid Man and Barnacle Boy",
            "publisher": "Paul",
            "category": "superhero",
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = {
            "title": "Mermaid Man and Barnacle Boy",
            "publisher": "Paul",
            "category": "superhero",
        }
        self.assertEqual(response.data, response_data)
        self.assertEqual(Book.objects.count(), 4)
        stored_book: Book = Book.objects.all()[3]
        self.assertEqual(stored_book.title, "Mermaid Man and Barnacle Boy")
        self.assertEqual(stored_book.publisher, "Paul")
        self.assertEqual(stored_book.category, "superhero")
        self.assertEqual(stored_book.borrow_duration, None)
        self.assertEqual(stored_book.due_back, None)
        self.assertEqual(stored_book.borrower, None)
        self.assertEqual(stored_book.status, "a")

    def test_remove_a_book_from_the_library(self):
        """Test removal of a book from the library."""
        self.assertEqual(Book.objects.count(), 3)
        url = reverse("delete-book", kwargs={"pk": 1})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_list_of_books_not_available(self):
        """List books not available."""
        url = reverse("borrowed-books")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["borrower"], "squidward.t@kk.com")
        self.assertEqual(response.data["results"][0]["status"], "b")
        self.assertEqual(response.data["results"][0]["borrow_duration"], 5)
        self.assertEqual(
            response.data["results"][0]["due_back"],
            str(timezone.now().date() + timezone.timedelta(days=5)),
        )
