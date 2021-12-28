import logging
import socket
import threading
import time

logging.basicConfig(filename='../communication/levelling_controller.log', filemode='w', format='%(asctime)s - %(message)s',
                    level=logging.DEBUG)
logging.debug('levelling start')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.1.11", 8080)
sock.connect(server_address)
sock.send("IDlevelling".encode())


def receive():
    while True:
        data = sock.recv(1024).decode()
        if data.startswith(("cmd", "init", "con")):
            logging.debug(data)
            print(data)
        elif data.startswith("Debug"):
            print(data)
            # logging.debug(data)


def send():
    count = 0
    while True:
        data = "DL100" + str(count)
        sock.send(data.encode())
        print("send data:", data)
        count += 1
        time.sleep(5)


threading.Thread(target=send).start()
threading.Thread(target=receive).start()
