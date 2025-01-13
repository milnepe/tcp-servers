#!/usr/bin/env python3
"""
A basic TCP socket server that handles a single connection request and responds with and ACK

Run: python tcp-server.py 127.0.0.1 65432
"""

import sys
import socket

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])

try:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Force the socket to reuse an existing connection even if it wan't closed properly
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            sock.bind((host, port))
            sock.listen()
            conn, addr = sock.accept()

            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    # No data means the client closed its connection, so the server can end its side
                    if not data:
                        break
                    print(data)
                    conn.sendall(b"ACK")
except KeyboardInterrupt:
    # Exit nicely, ensuring server socket is closed
    print("Caught keyboard interrupt, exiting")
finally:
    sock.close()
