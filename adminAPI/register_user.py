import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminAPI.settings")
django.setup()

import pika
import json
from user.models import User

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="broker"))
channel = connection.channel()

exchange_topic =  "admin_commands"
channel.exchange_declare(exchange=exchange_topic, exchange_type="topic")

result = channel.queue_declare("", exclusive=True)
queue_name = result.method.queue
binding_key = "adminapi.register_user"
channel.queue_bind(exchange=exchange_topic, queue=queue_name, routing_key=binding_key)


def register_new_user(ch, method, properties, data: str):
    """Register new user on the database"""
    user_data = json.loads(data)
    user = User.objects.create(**user_data)


channel.basic_consume(queue=queue_name, on_message_callback=register_new_user, auto_ack=True)

channel.start_consuming()
