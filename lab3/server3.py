IP_ADDR = "127.0.0.1"
DEST_PORT = 65435
PORT = 65435
BUF_SIZE = 1024
from socket import socket, AF_INET, SOCK_DGRAM, timeout
import time



def converter(num):
    if num*10%10 == 0:
        return int(num)
    return num


def divider(data):
    str = data.decode()
    expression = str.split(" ")
    sign = expression[0]
    a = expression[1]
    b = expression[2]
    return sign, a, b

def type_converter(num1):
    if num1.find('.') != -1:
        num1 = float(num1)
    else:
        num1 = int(num1)
    return num1



if __name__ == "__main__":
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.bind((IP_ADDR, PORT))
        # s.settimeout(5)
        # print(f"Server started: {time.time()}")
        try:
            while True:
                print("Waiting for a new file")
                try:
                    data, addr = s.recvfrom(BUF_SIZE)
                    command, seqno, extension, size = data.decode().split(" | ")
                    if command =="s":
                        # time.sleep(8)
                        respond = "ack"
                        print(respond)
                        s.sendto(respond.encode(), addr)

                except KeyError:
                    print('OOps')
                #
                # except ValueError:
                #
                #
                # except ZeroDivisionError:


        except KeyboardInterrupt:
            print(f"Server was stopped at {time.time()}")
