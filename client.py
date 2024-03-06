import socket
import constants
from config import app_config


def send_file(client_socket):
    with open(constants.save_file_path, 'rb') as file:
        file_data = file.read()
        file_size = len(file_data).to_bytes(4, byteorder='big')
        client_socket.send(file_size)
        client_socket.sendall(file_data)


def load(client_socket):
    # TODO: impl
    pass


def run_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        message = data.decode()
        # print(f"Received message: {message}")

        if message == 'save':
            send_file(client_socket)
        elif message == 'load':
            load(client_socket)


def get_server_ip():
    ip = app_config.get('network', 'ip')
    print(f"Previous server IP was {ip}, press ENTER or provide new IP")
    # TODO: add input validation
    user_input = input()

    if user_input == "":
        return ip

    app_config.set('network', 'ip', user_input)

    return ip


def start_client(server_ip: str):
    port = int(app_config.get('network', 'port'))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print(f"Client connected to {server_ip}:{port}")

    with client_socket:
        run_client(client_socket)


if __name__ == "__main__":
    server_ip = get_server_ip()
    start_client(server_ip)
