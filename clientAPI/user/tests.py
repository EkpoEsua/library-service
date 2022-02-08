from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User
from rest_framework import status
from books.models import Book


class ClientAPITestCase(APITestCase):
    def setUp(self) -> None:
        """Setup data for test methods."""
        # Create user in database
        User.objects.create(
            email="squidward.t@kk.com", first_name="Squidward", last_name="Tentacles"
        )

    def test_users_can_enroll_in_the_library(self):
        """Ensure a user can be register in the library using their email, first name, and last name."""
        url = reverse("register-user")
        data = {
            "email": "spongebob.s@kk.com",
            "first_name": "Spongebob",
            "last_name": "Squarepant",
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(pk=2).first_name, "Spongebob")
        self.assertEqual(User.objects.get(pk=2).last_name, "Squarepant")
        self.assertEqual(User.objects.get(pk=2).email, "spongebob.s@kk.com")
