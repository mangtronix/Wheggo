# Receive OSC messages over wifi with CircuitPython
# Includes minimalist OSC message parser
# Uses non-blocking socket code to receive the UDP packets
#
# Michael Ang <https://michaelang.com>
# For Outside Lab at New York University Abu Dhabi Interactive Media
# https://outside.nyuadim.com/
#
# MIT License
#
# Tested with FeatherS2 Neo - ESP32-S2
# https://unexpectedmaker.com/shop/feathers2neo-esp32s2

import wifi
import socketpool
import struct
import time

# Put your ssid and password in secrets.py
from secrets import secrets

# Port for incoming OSC connections
listen_port = 9000

# Connect to wifi
print("Connecting to wifi - {}".format(secrets['ssid']))
wifi.radio.connect(secrets['ssid'], secrets['password'])

print("My IP address is", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)

# Make a UDP socket
print("Creating UDP socket")
sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)

# Create a buffer for receiving packets
packet = bytearray(48)

def parse_osc_packet(packet_data, packet_size):
    '''Returns (route, msg_type, value) or raises ValueError'''
    # OSC message spec
    # https://hangar.org/wp-content/uploads/2012/01/The-Open-Sound-Control-1.0-Specification-opensoundcontrol.org_.pdf
    
    # XXX handle invalid packets better - we currently assume the packet is a valid OSC message
    
    route = str(packet_data[:packet_data.index(b'\x00')],'ascii')

    comma_index = packet_data.index(',')
    msg_type = str(packet_data[comma_index+1:comma_index+2],'ascii')
    
    value = None

    if msg_type == 'f':
        # float32 32-bit big-endian IEEE 754 floating point number
        value = struct.unpack_from('>f', packet_data, packet_size-4)[0]
    elif msg_type == 'i':
        # int32 - 32-bit big-endian two's complement integer
        value = struct.unpack_from('>i', packet_data, packet_size-4)[0]
    elif msg_type == 's':
        # A sequence of non-null ASCII characters followed by a null
        value = str(packet_data[comma_index + 4:], 'ascii')
        value = value.split('\0', 1)[0] # Take up to null
        
    else:
        raise ValueError("msg_type is {}, not implemented".format(msg_type))
        
    return (route, msg_type, value)

our_ip = str(wifi.radio.ipv4_address)
with pool.socket(pool.AF_INET, pool.SOCK_DGRAM) as s:
    print("Binding socket")
    s.bind((our_ip, listen_port))

    # Set the socket as non-blocking. If we ask to receive
    # data and there is none waiting we get an OSError and
    # can continue with our other code
    s.setblocking(False)


    print("Listening for OSC messages at {:s}:{}".format(our_ip, listen_port))
    while True:
        # print('Receiving')
        try:
            packet_size, address = s.recvfrom_into(packet)
        except OSError as e:
            # If there's no data we get an exception
            # print("Got error: " + str(e))
            continue
            
        # print("Received packet")
        # print('  ' + str(packet[:packet_size]))

        got_message = False
        try:
            (route, msg_type, value) = parse_osc_packet(packet, packet_size)
            print('  {} {} {}'.format(route, msg_type, value))
            got_message = True
            
        except ValueError as err:
            print(err)

        # If we got a message, immediately check again, otherwise sleep a bit 
        if not got_message:
            time.sleep(0.1)
        