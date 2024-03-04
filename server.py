import socket
import threading

# Function to broadcast a message to all connected clients
def broadcast(message, connections):
    for client_socket in connections:
        try:
            client_socket.send(message.encode())
        except:
            # Remove the client if unable to send the message
            connections.remove(client_socket)


def receive_file(conn, filename):
    print(f'> receive_file')
    with open(filename, 'wb') as file:
        data = conn.recv(1024)
        while data:
            file.write(data)
            data = conn.recv(1024)
    print(f'< receive_file')


def save():
    for client_socket in connections:
        try:
            client_socket.send('save'.encode())
            receive_file(client_socket, 'REDTMP')
        except:
            # Remove the client if unable to send the message
            connections.remove(client_socket)


connections = []


# Main server function
def start_server():
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 12345  # Choose a suitable port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Allow up to 5 queued connections

    print(f"Server listening on {host}:{port}")


    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        connections.append(client_socket)

# Start the server
server_thread = threading.Thread(target=start_server)
server_thread.start()

while True:
    print("Enter message to send to client:")
    user_input = input()
    print(f"user_input: {user_input}")
    if user_input == 'save':
        save()
    else:
        print('Invalid input!')
