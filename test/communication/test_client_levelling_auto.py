import logging
import socket
import threading
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.10.104", 8080)
sock.connect(server_address)
sock.send("IDlevel".encode())
time.sleep(2)
sock.send("L-STATUS-ready".encode())

def receive():
    while True:
        data = sock.recv(1024).decode().strip()
        if data == "Lbat":
            sock.sendall("L-INFO-Bat-7".encode())
        elif data == "Lcmd01t":
            time.sleep(2)
            sock.sendall("L-INFO-Stopped".encode())
        elif data == "Lcmd01L":
            time.sleep(3)
            sock.sendall("L-INFO-LevellingFinish".encode())
        # elif data == "Lstatus":
        #     sock.sendall("L-STATUS-ready")

threading.Thread(target=receive).start()
