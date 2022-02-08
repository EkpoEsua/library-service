import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminAPI.settings")
django.setup()

import pika
import json
from books.models import Book
from user.models import User

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="broker"))
channel = connection.channel()

exchange_topic =  "admin_commands"
channel.exchange_declare(exchange=exchange_topic, exchange_type="topic")

result = channel.queue_declare("", exclusive=True)
queue_name = result.method.queue
binding_key = "adminapi.borrow_book"
channel.queue_bind(exchange=exchange_topic, queue=queue_name, routing_key=binding_key)

def borrow_book(ch, method, properties, data: str,):
    """Mark a book as borrowed."""
    borrow_data = json.loads(data)
    book_to_borrow: Book = Book.objects.get(pk=int(borrow_data["id"]))
    book_to_borrow.status = borrow_data["status"]
    book_to_borrow.borrow_duration = borrow_data["borrow_duration"]
    user = User.objects.get(email=borrow_data["borrower_id"])
    book_to_borrow.borrower = user
    book_to_borrow.save()

channel.basic_consume(queue=queue_name, on_message_callback=borrow_book, auto_ack=True)

channel.start_consuming()
