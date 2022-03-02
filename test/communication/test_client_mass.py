import random
import socket
import threading
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.8.154", 8080)
sock.connect(server_address)
sock.send("IDmass".encode())
time.sleep(2)
sock.send("M-STATUS-ready".encode())


def receive():
    while True:
        command = sock.recv(1024).decode()
        print(command)
        if "Mass_move" in command:
            time.sleep(3)
            sock.sendall("M-INFO-MOVED\n".encode())
        elif "Mass_stop" in command:
            time.sleep(3)
            sock.sendall("M-INFO-STOPPED\n".encode())
        elif "Mass_getPos" in command:
            pos_data = generate_mass_data()
            sock.send(pos_data.encode())


def generate_mass_data():
    # simulate moving mass pos
    pos_list = [str(random.randint(0, 1000)) for i in range(2)]
    pos_data = "M-D-X{}Y{}\n".format(pos_list[0], pos_list[1])
    return pos_data


# threading.Thread(target=send).start()
threading.Thread(target=receive).start()
