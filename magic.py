#!/usr/bin/python3
import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument("--server_address",
    help="IP address of the Cockatrice server",
    default="127.0.0.1")
parser.add_argument("--server_port",
    help="TCP port of the Cockatrice server",
    default=4747,
    type=int)

args = parser.parse_args()

# Let's connect to the server
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((args.server_address, args.server_port))
sock.send("MESSAGE".encode())
data = sock.recv(BUFFER_SIZE)
sock.close()

print("data", data)
