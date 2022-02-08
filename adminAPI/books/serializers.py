import json
from rest_framework import serializers
from books.models import Book
from source import emit_command


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

    def save(self, **kwargs):
        instance: Book = super().save(**kwargs)
        instance_dict: dict = instance.__dict__
        instance_dict.pop("_state")
        emit_command(json.dumps(instance_dict), "clientapi.create_book")
        return instance


class BookBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "borrow_duration",
            "borrower",
        )
        extra_kwargs = {"borrower": {"help_text": "Registered email address of user."}}

    def update(self, instance: Book, validated_data):
        instance.status = "b"
        instance: Book = super().update(instance, validated_data)
        return instance
