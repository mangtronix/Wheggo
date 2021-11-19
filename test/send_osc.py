#!/usr/bin/env python

"""
Send OSC messages. Enter the destination IP address / port
in the arguments or from the command line.

Adapted from example at: https://pypi.org/project/python-osc/
"""
import argparse
import random
import time

from pythonosc import udp_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="192.168.8.51",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=9000,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    print("Connecting to server at {}:{}".format(args.ip, args.port))
    client = udp_client.SimpleUDPClient(args.ip, args.port)

    for x in range(10):
        print("Sending messages")
        client.send_message("/motor/1/speed", random.random())
        client.send_message('/command',random.choice(['forward', 'backward','left','right','stop']))
        client.send_message('/someinteger', random.randrange(-10,10))
        time.sleep(1)