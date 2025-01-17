"""
An Asyncio TCP client that prompts for specific user commands and send them to the server.
Any response is printed to stdout.

Connect the client and send ON or OFF commands to control the server.
The connection can be closed by entering the "STOP" command.

Usage:
    python -m client <HOST> <PORT>
"""

import asyncio
import sys
import json


async def run_client(host: str, port: int) -> None:
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except (ConnectionRefusedError, OSError) as e:
        print(f"Failed to connect to server at {host}:{port}: {e}")
        return

    while True:
        command = input("Enter command (ON, OFF or STOP): ")
        if command.strip() == "STOP":
            print("Received STOP, closing connection.")
            # Close the connection
            writer.write(b'')
            await writer.drain()
            break
        if command.strip() in ["ON", "OFF"]:
            message = json.dumps({"command": command.strip()})
            try:
                writer.write(message.encode() + b"\r\n")
                await writer.drain()
            except (BrokenPipeError, ConnectionResetError) as e:
                print(f"Failed to send message to server: {e}")
                break


async def main(host: str, port: int):
    client_task = asyncio.create_task(run_client(host, port))
    await client_task


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m client <HOST> <PORT>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    asyncio.run(main(host, port))
