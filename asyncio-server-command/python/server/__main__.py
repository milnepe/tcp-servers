"""
An Asyncio TCP server that responds to specific commands.

Connect a client and send 'ON' or 'OFF' commands to control the server.
All connected clients will receive the command.

Note: Commands must be terminated with a carriage return, newline pair (\r\n).

Test with nc:
printf "ON\r\n" | nc 127.0.0.1 65432
printf "OFF\r\n" | nc 127.0.0.1 65432

Usage:
    python -m server <HOST> <PORT>
"""

import sys
import asyncio
from socket import error as SocketError

clients = []


async def handler(reader, writer):
    client_address = writer.get_extra_info("peername")
    print(f"Client connected: {client_address}")
    clients.append(writer)

    try:
        while not reader.at_eof():
            data = await reader.readline()
            if not data:
                break
            message = data
            print(f"Message from {client_address}: {message}")

            if message == b"ON\r\n" or message == b"OFF\r\n":
                # Send the message to all connected clients
                for client in clients:
                    if not client.is_closing():
                        try:
                            if message == b"ON\r\n" or message == b"OFF\r\n":
                                client.write(message)
                            await client.drain()
                        except ConnectionError:
                            print(
                                f"Connection to {client.get_extra_info('peername')} closed while sending"
                            )

    except asyncio.exceptions.CancelledError:
        print(f"Connection with {client_address} closed")
    except SocketError as e:
        print(f"Connection with {client_address} reset: {e}")
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()
        print(f"Client disconnected: {client_address}")


async def run_server(host: str, port: int) -> None:
    server = await asyncio.start_server(
        handler, host, port, reuse_address=True, reuse_port=True
    )
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m server <HOST> <PORT>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    asyncio.run(run_server(host, port))
