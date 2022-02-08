from rest_framework import serializers
from user.models import User
from books.serializers import BookListSerializer


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
        )


class UsersandBorrowedBooksSerializer(serializers.ModelSerializer):
    borrowed_books = BookListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "borrowed_books")
