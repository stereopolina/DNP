import socket
import os
# lsof -i:65435
import socket
import time
from socket import socket, AF_INET, SOCK_DGRAM, timeout

DEST_IP_ADDR = "127.0.0.1"
DEST_PORT = 65435
PORT = 65436
BUF_SIZE = 1024
file = 'innopolis.jpg'




def file_to_start_message_converter(filename):
    return f's|0|{os.path.splitext(filename)[1]}|{(os.stat(filename).st_size)}'


def file_sender(file, s, max_size):
    seqno = 1
    flag = True
    with open(file, 'rb') as myfile:
        while flag:
            for i in range(0, 5):
                try:
                    # width= myfile.size[0]
                    # first_slice = int(width)*(seqno-1)
                    # second_slice = int(width)*seqno
                    data_bytes = myfile.read(int(max_size) - len(bytes(f'd|{seqno}| ', 'utf-8')))
                    # data_bytes = myfile.readlines()[first_slice:second_slice]
                    message = f'd|{seqno}|{data_bytes}'
                    s.sendto(message.encode(), (DEST_IP_ADDR, DEST_PORT))
                    if max_size * seqno == os.stat(file).st_size:
                        flag = 'finish'
                        print('File transmitted')
                    s.settimeout(0.5)
                    data, addr = s.recvfrom(BUF_SIZE)
                    seqno += 1
                    if data.decode().split('|')[0] == "a" and data.decode().split('|')[1] == f'{seqno}':
                        break
                    else:
                        if i == 5:
                            flag = False
                except timeout:
                    if i == 5:
                        flag = False
                    continue
            if (flag == False):
                print("The server must be done. I quit")
                flag = False
                break


    file.close()

if __name__ == "__main__":
    flag = True
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.bind(("localhost", PORT))
        try:
            while flag:
                for i in range(0, 5):
                    try:
                        start_message = file_to_start_message_converter(file)  # sends start message
                        s.sendto(start_message.encode(), (DEST_IP_ADDR, DEST_PORT))
                        s.settimeout(0.5)  # sets timeout after sending first message
                        data, addr = s.recvfrom(BUF_SIZE)
                        if data.decode().split('|')[0] == "a":
                            file_sender(file, s, data.decode().split('|')[2])
                            flag = False
                            break
                    except timeout:
                        continue
                if(flag==True):
                    print("The server must be done. I quit")
                    flag = False
                    break

            s.close()
        except KeyboardInterrupt:
            print(f"User quit at {time.time()}")


