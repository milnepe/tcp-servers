"""
An Asyncio TCP client that prompts for specific user commands and send them to the server.
Any response is printed to stdout.

Connect the client and send ON or OFF commands to control the server.
The connection can be closed by entering the "STOP" command.

Usage:
    python -m client <HOST> <PORT>
    python -m client 127.0.0.1 65432 
"""

import asyncio
import sys
import json
import uuid


async def run_client(host: str, port: int) -> None:
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except (ConnectionRefusedError, OSError) as e:
        print(f"Failed to connect to server at {host}:{port}: {e}")
        return

    mac = get_mac()

    while True:
        command_input = input("Enter command [ON, OFF, STOP] optional MAC [00:00:00:00:00:00]: ")
        parts = command_input.strip().split()
        command = parts[0]
        target_mac = parts[1] if len(parts) > 1 else None

        if command == "STOP":
            print("Received STOP, closing connection.")
            # Close the connection
            writer.write(b'')
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            break
        if command in ["ON", "OFF"]:
            message = {
                "command": command,
                "src_addr": mac
            }
            if target_mac:
                message["target_addr"] = target_mac

            try:
                writer.write(json.dumps(message).encode() + b"\r\n")
                await writer.drain()
            except (BrokenPipeError, ConnectionResetError) as e:
                print(f"Failed to send message to server: {e}")
                break


def get_mac() -> str:
    return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
    for ele in range(0,8*6,8)][::-1])

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
