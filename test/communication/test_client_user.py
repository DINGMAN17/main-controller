import logging
import socket
import threading
import time

logging.basicConfig(filename='../communication/user.log', filemode='w', format='%(asctime)s - %(message)s',
                    level=logging.DEBUG)
logging.debug('levelling start')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.1.11", 8080)
sock.connect(server_address)
sock.send("IDuser".encode())


def receive():
    while True:
        data = sock.recv(1024).decode()
        if data.startswith("DL"):
            logging.debug(data)
        elif data.startswith("Debug"):
            print(data)
            # logging.debug(data)


def send():
    while True:
        command = input()
        sock.send(command.encode())
        print("send data:", command)


threading.Thread(target=send).start()
threading.Thread(target=receive).start()