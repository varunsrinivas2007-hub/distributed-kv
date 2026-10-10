import socket


def send_to_node(host, port, message):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.settimeout(2)

    try:
        connection.connect((host, port))

        connection.sendall(message.encode())

        response = connection.recv(1024)

        return response.decode()

    finally:
        connection.close()
