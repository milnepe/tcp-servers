"""
Asyncio TCP server with independent reading and writing corouteens

Usage:
python -m server 192.168.1.235 3333
"""

import asyncio
import sys

DELAY_SECONDS = 10


async def reader_task(client_addr, streams):
    print("Starting reader task...")
    reader, writer = streams
    try:
        while True:
            data = await reader.readline()
            print(f"Reader received: {data}")
            if not data:
                print("Disconnecting writer")
                writer.close()
                await writer.wait_closed()
                return
    except Exception as e:
        print(f"{client_addr} reader task error: {e}")
    finally:
        print(f"Reader for {client_addr} finished")


async def sender_task(client_addr, streams):
    print("Starting writer task...")
    reader, writer = streams
    while True:
        try:
            await asyncio.sleep(DELAY_SECONDS)
            writer.write(("ACK\n").encode())
            await writer.drain()
        except Exception as e:
            print(f"Failed to send to {e}")
    print(f"Sender for {client_addr} finished")


async def handle_input(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    streams = (reader, writer)
    addr, port = writer.get_extra_info("peername")
    print(f"Connection from {addr}:{port}")

    await asyncio.gather(reader_task(addr, streams), sender_task(addr, streams))


async def run_server(host: str, port: int) -> None:
    server = await asyncio.start_server(
        handle_input, host, port, reuse_address=True, reuse_port=True
    )
    async with server:
        await server.serve_forever()

    await asyncio.gather(
        start_server())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python async-server.py <HOST> <PORT>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    print(f"Starting server on {host} {port}")

    try:
        asyncio.run(run_server(host, port))
    except KeyboardInterrupt:
        pass
