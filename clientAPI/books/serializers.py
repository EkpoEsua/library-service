from rest_framework import serializers
from books.models import Book
from source import emit_command
import json


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "status",
            "publisher",
            "category",
            "due_back",
            "borrow_duration",
            "borrower",
        )


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "title",
            "publisher",
            "category",
        )


class BookBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "borrow_duration",
            "borrower",
        )
        extra_kwargs = {
            "borrower": {
                "help_text": "Registered email address of user.",
                "required": True,
            },
            "borrow_duration": {"required": True},
        }

    def update(self, instance: Book, validated_data):
        instance.status = "b"
        instance: Book = super().update(instance, validated_data)
        instance_dict: dict = instance.__dict__
        instance_dict.pop("_state")
        instance_dict.pop("due_back")
        emit_command(json.dumps(instance_dict), "adminapi.borrow_book")
        return instance
