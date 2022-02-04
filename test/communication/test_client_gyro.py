import socket
import threading
import time


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.10.104", 8080)
sock.connect(server_address)
sock.send("IDgyro".encode())


def receive():
    while True:
        command = sock.recv(1024).decode()
        if command.startswith("G"):
            print(command)


def send():
    count = 0
    while True:
        data = "G100" + str(count)
        sock.send(data.encode())
        print("send data:", data)
        count += 1
        time.sleep(5)


threading.Thread(target=send).start()
threading.Thread(target=receive).start()