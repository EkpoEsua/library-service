import json
import requests
import unittest
from test_data import books, users

admin_api_connection = "http://localhost:8000"
client_api_connection = "http://localhost:9000"


class ClientAPITest(unittest.TestCase):

    def setUp(self) -> None:
        # Add books to the library from the admin API
        create_book_url = admin_api_connection + "/books/create/"
        for book in books:
            last_created_book = requests.post(create_book_url, data=book)

        # Add User
        register_users_url = client_api_connection + "/users/register/"
        user_data = users[0]
        registered_user = requests.post(register_users_url, data=user_data)

        # Borrow a book
        user = json.loads(registered_user.content)
        user_email = user["email"]
        book = json.loads(last_created_book.content)
        book_id = book["id"]
        borrow_book_url = client_api_connection + f"/books/{book_id}/borrow/"
        print(borrow_book_url, book_id, book)
        borrow_book_data = {
            "borrow_duration": 3,
            "borrower": user_email
        }
        borrowed_book = requests.put(borrow_book_url, data=borrow_book_data)

    def test_user_enrollment(self):
        """Test user enrollment on the client API."""
        url = client_api_connection + "/users/register/"
        data = users[1]
        response = requests.post(url, data=data)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertIs(type(response_data["id"]), int)
        self.assertEqual(response_data["email"], data["email"])
        self.assertEqual(response_data["first_name"], data["first_name"])
        self.assertEqual(response_data["last_name"], data["last_name"])

    def test_listing_of_all_available_books(self):
        """Test listing of all available books."""
        url = client_api_connection + "/books/"
        response = requests.get(url)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["count"], 4)
    
    