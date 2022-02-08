import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clientAPI.settings")
django.setup()

import pika
import json
from books.models import Book

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="broker"))
channel = connection.channel()

exchange_topic =  "client_commands"
channel.exchange_declare(exchange=exchange_topic, exchange_type="topic")

result = channel.queue_declare("", exclusive=True)
queue_name = result.method.queue
binding_key = "clientapi.create_book"
channel.queue_bind(exchange=exchange_topic, queue=queue_name, routing_key=binding_key)


def create_new_book(ch, method, properties, data: str):
    """Create a new book in the database."""
    print(data)
    book_data = json.loads(data)
    book = Book.objects.create(**book_data)

channel.basic_consume(queue=queue_name, on_message_callback=create_new_book, auto_ack=True)

channel.start_consuming()

