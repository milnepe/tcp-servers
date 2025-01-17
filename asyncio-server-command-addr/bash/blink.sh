#! /bin/bash
# Blink the esp leds
# Creates a new client socket each time which times out after 1 second

while :
do
	printf '{"command": "ON"}\r\n' | nc -w 127.0.0.1 65432
	printf '{"command": "OFF"}\r\n' | nc -w 127.0.0.1 65432
done

