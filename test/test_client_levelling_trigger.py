import logging
import socket
import threading
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 8080)
sock.connect(server_address)
sock.send("IDlevelling".encode())


def receive():
    count = 0
    while True:
        data = sock.recv(1024).decode()
        if data.startswith(("cmd", "init", "co", "ba")):
            print(data)
        elif data.startswith("sensor"):
            data = "DL100" + str(count)
            sock.send(data.encode())
            print("send data: " + data)
            count += 1


threading.Thread(target=receive).start()
