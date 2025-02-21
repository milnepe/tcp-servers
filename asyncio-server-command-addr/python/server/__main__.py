"""
An Asyncio TCP server that responds to specific commands.

Connect a client and send 'ON' or 'OFF' commands to control the server.
If the optional target mac address is included then a specific client will receive the command
otherwise all connected clients will receive the command.

Note: Commands must be terminated with a carriage return, newline pair (\r\n).

Test with nc:
printf '{"command": "ON", "target_addr": "aa:bb:cc:dd:ee:ff"}\r\n' | nc 127.0.0.1 65432
printf '{"command": "OFF", "target_addr": "aa:bb:cc:dd:ee:ff"}\r\n' | nc 127.0.0.1 65432

Usage:
    python -m server <HOST> <PORT>
"""

import logging
import sys
import asyncio
import json
from socket import error as SocketError

VERSION = "0.0.1"

logger = logging.getLogger("srv")
logging.basicConfig()

log_levels = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}

clients = {}


async def handler(reader, writer):
    client_address = writer.get_extra_info("peername")
    logger.info(f"Client connected: {client_address}")

    try:
        while not reader.at_eof():
            data = await reader.readline()
            if not data:
                break
            message = data.decode().strip()
            logger.info(f"Message from {client_address}: {message}")

            try:
                message_json = json.loads(message)
            except json.JSONDecodeError:
                logger.info(f"Failed to decode JSON message from {client_address}: {message}")
            src_addr = message_json.get("src_addr")
            command = message_json.get("command")
            target = message_json.get("target_addr")

            if src_addr:
                clients[src_addr] = writer

            if command in ["ON", "OFF"]:
                # Send the message to a single client
                if target and target in clients:
                    client_writer = clients[target]
                    if  not client_writer.is_closing():
                        try:
                            client_writer.write(command.encode() + b"\r\n")
                            await client_writer.drain()
                        except ConnectionError:
                            logger.info(f"Connection to {client_writer.get_extra_info('peername')} closed")
                else:
                    # Send the message to all connected clients
                    for _, client_writer in clients.items():
                        if  not client_writer.is_closing():
                            try:
                                client_writer.write(command.encode() + b"\r\n")
                                await client_writer.drain()
                            except ConnectionError:
                                logger.info(f"Connection to {client_writer.get_extra_info('peername')} closed while sending")

    except asyncio.exceptions.CancelledError:
        logger.error(f"Connection with {client_address} closed")
    except SocketError as e:
        logger.error(f"Connection with {client_address} reset: {e}")
    except Exception as e:
        logger.error(f"Error with {client_address}: {e}")


async def run_server(host: str, port: int) -> None:
    server = await asyncio.start_server(
        handler, host, port, reuse_address=True, reuse_port=True
    )
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        logger.critical(f"Usage: {sys.argv[0]} <HOST> <PORT> <LOG_LEVEL>")
        sys.exit(1)

    HOST, PORT, LOG_LEVEL = sys.argv[1], int(sys.argv[2]), sys.argv[3]

    log_level = log_levels.get(LOG_LEVEL, logging.INFO)
    logger.setLevel(log_level)

    logger.info(f"Local Server {VERSION}")

    asyncio.run(run_server(HOST, PORT))
