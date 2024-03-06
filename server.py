import os
import shutil
import socket
import threading
from client import start_client

connections = []


def receive_file(conn, path):
    # Receive file size
    file_size = int.from_bytes(conn.recv(4), byteorder='big')

    # Receive file data
    received_data = b''
    while len(received_data) < file_size:
        received_data += conn.recv(1024)

    # Save the received file
    with open(path, 'wb') as received_file:
        received_file.write(received_data)


def save(name: str):
    tmp_path = os.path.join('saves', 'tmp')
    shutil.rmtree(tmp_path, ignore_errors = True)

    for count, client_socket in enumerate(connections):
        player = f"player{count + 1}"
        player_path = os.path.join(tmp_path, player)
        os.makedirs(player_path, exist_ok = True)
        try:
            client_socket.send('save'.encode())
            receive_file(client_socket, os.path.join(player_path, 'REDTMP'))
        except:
            # Remove the client if unable to send the message
            connections.remove(client_socket)

    save_path = os.path.join('saves', name)
    shutil.rmtree(save_path, ignore_errors = True)

    os.rename(tmp_path, os.path.join('saves', name))


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


if __name__ == "__main__":
    # Start the server
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # client_thread = threading.Thread(target=start_client, args=('127.0.0.1',))
    # client_thread.start()

    while True:
        print("Type (S)ave or (L)oad and press ENTER:")
        user_input = input().lower()
        if user_input in ('save', 's'):
            save('default')
        if user_input in ('load', 'l'):
            pass

