import socket
import constants
from configparser import ConfigParser

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
        try:
            data = client_socket.recv(1024)
            message = data.decode()
            print(f"Received message: {message}")

            if message == 'save':
                send_file(client_socket)
            elif message == 'load':
                load(client_socket)
            else:
                print('Command not supported!')

        except Exception as e:
            print(e)
            break


def get_server_ip():
    config = ConfigParser()
    config.read('config.ini')

    ip = config.get('Network', 'ip')
    print(f"Previous server IP was {ip}, press ENTER or provide new IP")
    # TODO: add input validation
    user_input = input()

    if user_input == "":
        return ip

    config.set('Network', 'ip', user_input)
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

    return ip


def start_client(server_ip: str):
    config = ConfigParser()
    config.read('config.ini')
    port = int(config.get('Network', 'port'))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print("connected")

    with client_socket:
        run_client(client_socket)


if __name__ == "__main__":
    server_ip = get_server_ip()
    start_client(server_ip)
