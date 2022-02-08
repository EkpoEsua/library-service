import pika


def emit_command(message: str, routing_key: str, exchange: str = "admin_commands"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="broker"))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type="topic")

    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    connection.close()
