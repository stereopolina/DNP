# import binascii
# import json
#
# def get_crc_checksum(file_contents):
#     file_contents = (binascii.crc32(file_contents) & 0xFFFFFFFF)
#     return "%08X" % file_contents
#

# encoding: utf-8
import socket
import os

import socket
import time
from socket import socket, AF_INET, SOCK_DGRAM, timeout

DEST_IP_ADDR = "127.0.0.1"
DEST_PORT = 65435
PORT = 65436
BUF_SIZE = 1024



if __name__ == "__main__":
    proc = True
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.bind(("localhost", PORT))
        try:
            while proc:
                message = input("Input start message in the format s | seqno0 | extension | size:")
                for i in range(0, 5):
                    s.settimeout(5)
                    if message == "quit" or message == "Quit" or message == "QUIT":
                        s.close()
                        print("User has quit")
                        break
                    s.sendto(message.encode(), (DEST_IP_ADDR, DEST_PORT))
                    try:
                        data, addr = s.recvfrom(BUF_SIZE)
                        if data.decode() == "ack":
                    #print("Hello")


                        # print("Hello")
                #         starts transmitting the data
                    except timeout:
                        proc = False
                        print(f"Timeout expired:{time.time()}, Client decided that the server is down")
                        break


            s.close()
        except KeyboardInterrupt:
            print(f"User quit at {time.time()}")