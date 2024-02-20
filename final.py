import tkinter as tk
import threading
from rabbit import Rabbit
from json import loads, dumps
from argparse import ArgumentParser

class ChatApp:
    def __init__(self, username, target, channel):
        self.rabbit = Rabbit(username, target, channel)
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"Chat: {username}")

        # Create a text widget to display messages
        self.text_widget = tk.Text(self.root, height=20, width=50, state=tk.DISABLED)
        self.text_widget.pack(padx=10, pady=10)

        # Create an entry widget for typing messages
        self.entry = tk.Entry(self.root, width=20)
        self.entry.pack(padx=10, pady=(0, 10))

        # Send button with a modern style
        self.send_button = tk.Button(
            self.root,
            text="Send",
            command=self.send,
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT
        )
        self.send_button.pack(pady=(0, 10))

        # Start the consumer thread
        self.consumer_thread = threading.Thread(
            target=self.consumer_loop,
            name="consumer"
        )
        self.consumer_thread.start()

        self.root.mainloop()

    def consumer_loop(self):
        self.rabbit.consumer(self.callback)

    def send(self):
        message = self.entry.get()
        if message:
            self.rabbit.sender(message=message)
            self.entry.delete(0, tk.END)

    def callback(self, ch, method, properties, body):
        try:
            data = loads(body.decode())
            msg = f'{data["user"]}: {data["message"]}'
            self.update_text_widget(msg)
        except Exception as e:
            print("Error in callback:", e)

    def update_text_widget(self, text):
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"\n{text}")
        self.text_widget.see(tk.END)  # Scroll to the end
        self.text_widget.configure(state=tk.DISABLED)

# Define command-line arguments
parser = ArgumentParser(prog="Chat")
parser.add_argument("username", help="Username to connect as")
parser.add_argument("target", help="RabbitMQ server to connect to")
args = parser.parse_args()

CHANNEL = "chatroom"

if __name__ == "__main__":
    username = args.username
    target = args.target

    app = ChatApp(username, target, CHANNEL)
