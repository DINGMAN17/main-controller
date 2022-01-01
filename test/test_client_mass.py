import socket
import threading
import time


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.10.104", 8080)
sock.connect(server_address)
sock.send("IDmass".encode())


def receive():
    while True:
        command = sock.recv(1024).decode()
        if command.startswith("Mass"):
            print(command)


def send():
    count = 0
    while True:
        data = "DM100" + str(count)
        sock.send(data.encode())
        print("send data:", data)
        count += 1
        time.sleep(7)


threading.Thread(target=send).start()
threading.Thread(target=receive).start()
