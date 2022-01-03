import logging
import socket
import threading
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.10.104", 8080)
sock.connect(server_address)
sock.send("IDlevelling".encode())


def receive():
    while True:
        data = sock.recv(1024).decode()
        if data.startswith("L"):
            logging.debug(data)
        elif data.startswith("Debug"):
            print(data)
            # logging.debug(data)


def send():
    count = 0
    while True:
        data = "L100" + str(count)
        sock.send(data.encode())
        print("send data:", data)
        count += 1
        time.sleep(8)


threading.Thread(target=send).start()
threading.Thread(target=receive).start()
