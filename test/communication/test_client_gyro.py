import random
import socket
import threading
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.8.154", 8080)
sock.connect(server_address)
sock.send("IDgyro".encode())
time.sleep(1)
sock.send("G-STATUS-ready\n".encode())


def receive():
    while True:
        command = sock.recv(1024).decode()
        print(command)
        if "AutoOn" in command:
            time.sleep(2)
            sock.send("G-INFO-AUTOON\n".encode())
        elif "AutoOff" in command:
            time.sleep(2)
            sock.send("G-INFO-AUTOOFFSELECT\n".encode())
        elif "Stop" in command:
            time.sleep(3)
            sock.sendall("G-INFO-STOPPED\n".encode())
        elif "GetYaw" in command:
            data = generate_gyro_data()
            sock.sendall(data.encode())


def generate_gyro_data():
    # simulate moving mass pos
    num = random.uniform(-120, 120)
    gyro_data = "G-D-{:.2f}\n".format(num)
    return gyro_data


threading.Thread(target=receive).start()
