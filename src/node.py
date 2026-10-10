import sys
import socket
from config import nodes
from core import KVStore
from commands import execute
from replication import send_to_node


class Node:
    def __init__(self, node_id, config):
        self.node_id = node_id
        self.host = config["host"]
        self.port = config["port"]
        self.role = config["role"]
        self.followers = config["followers"]
        self.store = KVStore()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        print(f"Node {self.node_id} listening on {self.host}:{self.port}")
        try:
            while True:
                connection, address = self.server.accept()

                print(f"Connection received from {address}")

                while True:
                    data = connection.recv(1024)

                    if not data:
                        break

                    message = data.decode()
                    response = execute(message, self.store)

                    if response == "OK" and self.role == "leader":
                        self.replicate(message)

                    connection.sendall(response.encode())

                connection.close()

        except KeyboardInterrupt:
            print(f"\nNode {self.node_id} shutting down.")

        finally:
            self.server.close()

    def replicate(self, message):
        for follower_id in self.followers:
            follower_config = nodes[follower_id]

            try:
                response = send_to_node(
                    follower_config["host"],
                    follower_config["port"],
                    message,
                )

                print(f"Replication to Node {follower_id}: {response}")

            except (OSError, TimeoutError) as error:
                print(f"Replication to Node {follower_id} failed: {error}")


if len(sys.argv) != 2:
    print("Error: node ID is required.")
    print("Usage: python src/node.py <node_id>")
    sys.exit(1)

try:
    node_id = int(sys.argv[1])
except ValueError:
    print("Error: node ID must be an integer.")
    sys.exit(1)

if node_id not in nodes:
    print(f"Error: node {node_id} does not exist in the cluster.")
    sys.exit(1)

node_config = nodes[node_id]
node = Node(node_id, node_config)
node.start()
