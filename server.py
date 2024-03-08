import os
import re
import shutil
import socket
import threading
from client import start_client
from src.config import app_config
from src.network import receive_file, send_file

connections = []


def remove_stale_connections():
    for client_socket in connections:
        try:
            client_socket.send('connection_check'.encode())
        except:
            # Remove the client if unable to send the message
            connections.remove(client_socket)


def save(name: str):
    tmp_path = os.path.join('saves', 'tmp')
    shutil.rmtree(tmp_path, ignore_errors = True)

    for count, client_socket in enumerate(connections):
        player = f"player{count + 1}"
        player_path = os.path.join(tmp_path, player)
        os.makedirs(player_path, exist_ok = True)
        client_socket.send('save'.encode())
        receive_file(client_socket, os.path.join(player_path, 'REDTMP'))

    save_path = os.path.join('saves', name)
    shutil.rmtree(save_path, ignore_errors = True)

    os.rename(tmp_path, os.path.join('saves', name))
    app_config.set('misc', 'last_save_name', name)


def get_all_folders(path):
    return [entry.name for entry in path.iterdir() if entry.is_dir()]


def load(name: str):
    save_path = os.path.join('saves', name)
    if not os.path.isdir(save_path):
        print('Save does not exist!')
        return
    for count, connection in enumerate(connections):
        player = f'player{count + 1}'
        player_save_path = os.path.join(save_path, player, 'REDTMP')
        connection.send('load'.encode())
        send_file(connection, player_save_path)


def start_server():
    host = '0.0.0.0'  # Listen on all available interfaces
    port = int(app_config.get('network', 'port'))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(7)  # Allow up to 7 queued connections

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        connections.append(client_socket)


def is_valid_folder_name(folder_name):
    # Allow alphanumeric characters, spaces, underscores, and hyphens
    pattern = r"^[a-zA-Z0-9 _-]{1,255}$"
    return bool(re.match(pattern, folder_name))


def get_save_name():
    while True:
        remove_stale_connections()

        player_count = len(connections)
        latest_save_name = app_config.get('misc', 'last_save_name')
        print(f'Player count: {player_count}')
        print(f'Last save name was "{latest_save_name}", press ENTER or provide a new one or (C)ancel:')

        user_input = input()
        if user_input.lower() in ('cancel', 'c'):
            break
        if user_input.lower() == 'tmp':
            print('"tmp" is invalid save name!')
            continue
        if is_valid_folder_name(user_input):
            return user_input
        if user_input == '':
            return latest_save_name


if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    client_thread = threading.Thread(target=start_client, args=('127.0.0.1',))
    client_thread.start()

    while True:
        print("Type (S)ave or (L)oad and press ENTER:")
        user_input = input().lower()
        if user_input in ('save', 's'):
            save_name = get_save_name()
            save(save_name)
        if user_input in ('load', 'l'):
            save_name = get_save_name()
            load(save_name)
