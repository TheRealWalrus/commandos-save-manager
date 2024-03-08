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


def send_file(conn, path):
    with open(path, 'rb') as file:
        file_data = file.read()
        file_size = len(file_data).to_bytes(4, byteorder='big')
        conn.send(file_size)
        conn.sendall(file_data)
