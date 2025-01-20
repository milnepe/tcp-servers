#! /bin/bash
# Blink the esp leds
# Creates a new client socket each time which times out after 2 second

HOST=$1
PORT=$2

while :
do
	printf '{"command": "ON", "target_addr": "f0:24:f9:59:1f:60"}\r\n' | nc -w 2 $HOST $PORT
	printf '{"command": "OFF", "target_addr": "f0:24:f9:59:1f:60"}\r\n' | nc -w 2 $HOST $PORT
	printf '{"command": "ON", "target_addr": "a0:dd:6c:02:f2:cc"}\r\n' | nc -w 2 $HOST $PORT
	printf '{"command": "OFF", "target_addr": "a0:dd:6c:02:f2:cc"}\r\n' | nc -w 2 $HOST $PORT
	printf '{"command": "ON"}\r\n' | nc -w 2 $HOST $PORT
	printf '{"command": "OFF"}\r\n' | nc -w 2 $HOST $PORT
done
