"""
An Asyncio TCP client that prompts for specific user commands and send them to the server.
Any responce is printed to stdout.

Connect the client and send ON or OFF commands to control the server.
The connection can be closed by entering the "STOP" command.

Usage:
    python -m client <HOST> <PORT>
"""

import asyncio
import sys


async def run_client(host: str, port: int) -> None:
    reader, writer = await asyncio.open_connection(host, port)

    try:
        while True:
            command = input("Enter command (ON, OFF or STOP): ")
            if command.strip() == "STOP":
                print("Received STOP, closing connection.")
                # Close the connection
                writer.write(b"")
                await writer.drain()
                break
            if command.strip() == "ON" or command.strip() == "OFF":
                writer.write(command.encode() + b"\r\n")
                await writer.drain()

                data = await reader.readline()

                if not data:
                    raise Exception("Socket closed")

                message = data.decode()
                print(f"Received: {message!r}")
    finally:
        writer.close()
        await writer.wait_closed()


async def main(host: str, port: int):
    client_task = asyncio.create_task(run_client(host, port))
    await client_task


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python async-client.py <HOST> <PORT>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    asyncio.run(main(host, port))
