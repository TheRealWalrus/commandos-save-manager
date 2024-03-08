import re
import socket
import src.constants as constants
from src.config import app_config
from src.network import send_file, receive_file


def run_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        message = data.decode()
        # print(f"Received message: {message}")

        if message == 'save':
            send_file(client_socket, constants.save_file_path)
        elif message == 'load':
            receive_file(client_socket, constants.save_file_path)


def is_valid_ip(address):
    # Allow alphanumeric characters, spaces, underscores, and hyphens
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    return bool(re.match(pattern, address))


def get_server_ip():
    ip = app_config.get('network', 'ip')
    while True:
        print(f"Previous server IP was {ip}, press ENTER or provide new IP")
        user_input = input()
        if is_valid_ip(user_input):
            app_config.set('network', 'ip', user_input)
            return user_input
        if user_input == "":
            return ip
        print('Invald IP address!')


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
