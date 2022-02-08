import json
from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User
from rest_framework import status
from books.models import Book


class AdminAPITestCase(APITestCase):
    def setUp(self) -> None:
        """Setup data for test methods."""
        # Create users in database
        squid = User.objects.create(
            email="squidward.t@kk.com", first_name="Squidward", last_name="Tentacles"
        )
        sandy = User.objects.create(
            email="sandy.c@kk.com", first_name="Sandy", last_name="Cheeks"
        )

        # Create books in the database
        self.book1: Book = Book.objects.create(
            title="Just One Bite", publisher="Jay Lender", category="comedy"
        )
        self.book2: Book = Book.objects.create(
            title="Jellyfish Jam", publisher="Ennio", category="horror", status="b"
        )
        book3: Book = Book.objects.create(
            title="Sandy's Rocket", publisher="Cohen", category="science"
        )
        book4: Book = Book.objects.create(
            title="Mermaid Man and Barnacle Boy", publisher="Cohen", category="science"
        )

        # Borrow users some books
        self.book1.borrower = squid
        self.book1.borrow_duration = 4
        self.book1.save()
        self.book2.borrower = squid
        self.book2.borrow_duration = 5
        self.book2.save()
        book3.borrower = sandy
        book3.borrow_duration = 10
        book3.save()
        book4.borrower = sandy
        book4.borrow_duration = 5
        book4.save()

    def test_list_of_registered_users_in_the_library(self):
        """List registered users in the library."""
        url = reverse("list-users")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        first_user: User = User.objects.get(pk=1)
        first_user_dict = {
            "email": first_user.email,
            "first_name": first_user.first_name,
            "last_name": first_user.last_name,
        }
        self.assertEqual(dict(response.data["results"][0]), first_user_dict)

    def test_list_of_registered_users_and_borrowed_books(self):
        """Test user list and books they have borrowed."""
        url = reverse("users-and-borrowed-books")
        response = self.client.get(url, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["count"], 2)
        squid_data = {
            "email": "squidward.t@kk.com",
            "first_name": "Squidward",
            "last_name": "Tentacles",
            "borrowed_books": [
                {
                    "id": 1,
                    "title": "Just One Bite",
                    "status": "a",
                    "publisher": "Jay Lender",
                    "category": "comedy",
                    "due_back": str(self.book1.due_back),
                    "borrow_duration": 4,
                    "borrower": "squidward.t@kk.com",
                },
                {
                    "id": 2,
                    "title": "Jellyfish Jam",
                    "status": "b",
                    "publisher": "Ennio",
                    "category": "horror",
                    "due_back": str(self.book2.due_back),
                    "borrow_duration": 5,
                    "borrower": "squidward.t@kk.com",
                },
            ],
        }
        
        self.assertEqual(response_data["results"][0], squid_data)
