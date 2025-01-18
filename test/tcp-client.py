#!/usr/bin/env python3
"""
Test TCP client which sends and receives a single message string then disconnects

Run: tcp-test-client.py 127.0.0.1 65432
"""

import sys
import socket

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Ensures the client socket gets closed if something goes wrong with send or recv
    sock.settimeout(1)

    sock.connect((host, port))
    sock.sendall(b"Hello, world\r\n")
    data = sock.recv(1024)

print(f"Received {data!r}")
