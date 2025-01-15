"""
An asyncio client that connects to the server, sends a message, and waits
for an 'ACK' message before closing the connection.

Usage:
    python -m test <HOST> <PORT>
"""

import asyncio
import sys


async def run_client(host: str, port: int) -> None:
    reader, writer = await asyncio.open_connection(host, port)

    writer.write(b"Hello world!\r\n")
    await writer.drain()

    while True:
        data = await reader.read(1024)

        if not data:
            raise Exception("Socket closed")

        message = data.decode()
        print(f"Received: {message!r}")

        if message.strip() == "STOP":
            print("Received STOP, closing connection.")
            writer.close()
            await writer.wait_closed()
            break


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
