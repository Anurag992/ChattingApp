# Import the required libraries
from rabbit import Rabbit  
import threading         
from json import loads, dumps  
import argparse       

#source:Parser-Python,2023
#https://docs.python.org/3/library/argparse.html

# Define command-line arguments
parser = argparse.ArgumentParser(
                    prog='chat')  # Create an argument parser with a program name
parser.add_argument("username", help="Username to connect as")  # Add a required argument: username
parser.add_argument("target", help="RabbitMQ server to connect to")  # Add a required argument: target
args = parser.parse_args()  # Parse the command-line arguments and store them in "args"

CHANNEL = "chatroom"  # Define a constant named "CHANNEL" with the value "chatroom"

# Define a callback function to handle received messages
def __callback(self, ch, method, properties, body):
    try:
        data = loads(body.decode())  # Decode the message body and parse it as JSON
        if data["user"] == self.username:
            print(f"You: {data['message']}")  # Print the message if it's from the current user
        else:
            print(f"{data['user']}: {data['message']}")  # Print the message if it's from another user
    except:
        print("Friend:", body.decode())  # Print the message if it couldn't be parsed as JSON


#source:freeCodeCamp,2020
#https://www.freecodecamp.org/
# Define the main function
def main():
    # Create an instance of the Rabbit class with the provided username, target, and channel
    rabbit = Rabbit(args.username, args.target, CHANNEL)

    # Create a receiver thread that runs the "consumer" method of the Rabbit instance
    receiver = threading.Thread(target=rabbit.consumer, name="receiver")
    receiver.start()  # Start the receiver thread

    # Create a sender thread that runs the "sender" method of the Rabbit instance
    sender = threading.Thread(target=rabbit.sender, name="sender")
    sender.start()  # Start the sender thread

    receiver.join()  # Wait for the receiver thread to finish


#
# Entry point of the script
if __name__ == "__main__":
    main()  # Call the main function if the script is executed directly
