import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 8080)
sock.connect(server_address)
sock.send("IDlevelling".encode())


def receive():
    count = 0
    while True:
        data = sock.recv(1024).decode()
        if data.startswith("Lsensor"):
            data = "L100" + str(count)
            sock.send(data.encode())
            print("send data: " + data)
            count += 1

        elif data.startswith("L"):
            print(data)


threading.Thread(target=receive).start()
