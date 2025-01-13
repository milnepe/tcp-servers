"""
A simple multi-threaded TCP server that listens on a given port and sends and 'ACK' whenever it receives.

Usage:
    python async-server.py <HOST> <PORT>
"""
import asyncio
import sys

async def handle_input(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    while True:
        data = await reader.read(1024)
        if not data:
            break

        addr, port = writer.get_extra_info("peername")
        print(f"Received {data!r} from {addr}:{port}")

        writer.write(b"ACK")
        await writer.drain()

    writer.close()
    await writer.wait_closed()


async def run_server(host: str, port: int) -> None:
    server = await asyncio.start_server(handle_input, host, port, reuse_address=True, reuse_port=True)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python async-server.py <HOST> <PORT>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_server(host, port))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
