import pika 
from json import loads, dumps
from time import sleep


#source:Pika,2023
#https://pika.readthedocs.io/en/stable/#
#Pika — pika 1.3.2 documentation. (2023). Readthedocs.io. https://pika.readthedocs.io/en/stable/#
class Rabbit:
    def __init__(self, username, target, channel):
        # Initialize the class with user-defined username, target server, and communication channel
        self.username = username  # Store the username
        self.target = target      # Store the target RabbitMQ server address
        self.channelName = channel  # Store the name of the channel

    def __create_connection(self):
        # Create a connection to the RabbitMQ server and a channel
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.target))
        channel = connection.channel()
        # Declare a queue using the channel for communication
        channel.queue_declare(queue=self.channelName)
        return channel, connection

    def __callback(self, ch, method, properties, body):
        try:
            # Attempt to decode the received message as JSON
            data = loads(body.decode())
            if data["user"] == self.username:
                print(f"You: {data['message']}")
            else:
                print(f"{data['user']}: {data['message']}")
        except:
            # If decoding or other issues occur, print the message as-is
            print("Friend:", body.decode())


            # Send messages to the channel
    def sender(self, user=None, message=None):
        if not user:
            user = self.username
        channel, connection = self.__create_connection()
        if message:
            # If a message is provided, send it to the channel as a JSON payload
            channel.basic_publish(exchange='', routing_key=self.channelName, body=dumps({"user": user, "message": message}))
            connection.close()
            return
        while True:
            message = input()
            if message.lower() == 'exit':
                # If the user types 'exit', send a message indicating they've left
                channel.basic_publish(exchange='', routing_key=self.channelName, body="User has left the chat.")
                connection.close()
                break
            # Send the user's input as a message to the channel
            channel.basic_publish(exchange='', routing_key=self.channelName, body=dumps({"user": user, "message": message}))
        connection.close()


        # Consume messages from the channel and process them using the provided callback
    def consumer(self, callback=None):
        channel, _ = self.__create_connection()
        print("consume")
        if not callback:
            callback = self.__callback
        # Start consuming messages from the channel using the provided callback
        channel.basic_consume(queue=self.channelName, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

    # def consume():
