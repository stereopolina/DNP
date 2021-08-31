IP_ADDR = "127.0.0.1"
DEST_PORT = 65435
PORT = 65435
BUF_SIZE = 1024
from socket import socket, AF_INET, SOCK_DGRAM, timeout
import time
IMAGES = dict()
seqno_0 = 0
seqno = 0

def get_file(s):
    seqno = 1
    flag = True
    while flag:
        data, addr = s.recvfrom(BUF_SIZE + 50)
        command, seqno, data_bytes = data.decode().split("|")
        seqno = int(seqno)
        if command == 'd':
            IMAGES[seqno] = data_bytes
            seqno += 1
            respond = f"a|{seqno}|{BUF_SIZE}"
            s.sendto(respond.encode(), addr)
        if (flag == False):
            print("The server has quit")
            flag = False
            break

if __name__ == "__main__":
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.bind((IP_ADDR, PORT))
        # s.settimeout(5)
        # print(f"Server started: {time.time()}")
        try:
            while True:
                print("Waiting for a new file")
                data, addr = s.recvfrom(BUF_SIZE + 50)
                command, seqno, extension, size = data.decode().split("|")
                if command =="s":
                    # time.sleep(8)
                    respond = f"a|{seqno}|{BUF_SIZE}"
                    s.sendto(respond.encode(), addr)
                    get_file(s)




        except KeyboardInterrupt:
            print(f"Server was stopped at {time.time()}")


