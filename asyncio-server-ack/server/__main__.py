"""
An Asyncio TCP server that sends an 'ACK' message every second to each connected client
while receiving messages from them.

Usage:
    python -m server <HOST> <PORT>
"""

import sys
import asyncio


async def handler(reader, writer):
    client_address = writer.get_extra_info("peername")
    print(f"Client connected: {client_address}")

    async def send_message():
        while not writer.is_closing():
            try:
                writer.write(b"ACK")
                await writer.drain()
                await asyncio.sleep(1)
            except ConnectionError:
                print(f"Connection to {client_address} closed while sending")
                break

    # Start the message sender
    asyncio.create_task(send_message())

    # Receive messages from the client
    try:
        while not reader.at_eof():
            data = await reader.readline()
            if not data:
                break
            print(f"Message from {client_address}: {data.decode().strip()}")
    except asyncio.exceptions.CancelledError:
        print(f"Connection with {client_address} closed")
    except Exception as e:
        print(f"Error with {client_address}: {e}")


async def run_server(host: str, port: int) -> None:
    server = await asyncio.start_server(
        handler, host, port, reuse_address=True, reuse_port=True
    )
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python async-server.py <HOST> <PORT>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    try:
        asyncio.run(run_server(host, port))
    except KeyboardInterrupt:
        pass
