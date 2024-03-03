import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received message: {data.decode()}")
        except:
            break

def start_client():
    host = 'localhost'  # Change this to the server's IP address or hostname
    port = 12345  # Use the same port as the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Create a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("Enter message to send to server (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        try:
            client_socket.send(message.encode())
        except:
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
