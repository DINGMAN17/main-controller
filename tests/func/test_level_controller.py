import socket
import threading
import time
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('172.23.10.38', 8080)
sock.connect(server_address)
sock.send("IDlevel".encode())
time.sleep(2)
sock.send("L-STATUS-ready\n".encode())


def receive():
    while True:
        command = sock.recv(1024).decode().strip()
        print(command)
        if "Lbat" in command:
            sock.sendall("L-INFO-Bat-7\n".encode())
        elif "Lcmd01t" in command:
            time.sleep(1)
            sock.sendall("L-INFO-Stopped\n".encode())
        elif "Lcmd01K" in command:
            print("keep level running")
        elif "Lcmd01L" in command:
            time.sleep(5)
            sock.sendall("L-INFO-LevellingFinish\n".encode())
        elif "Lcmd06A" in command:
            print("sent auto finished")
            time.sleep(3)
            sock.sendall("L-INFO-AutoMoveFinish\n".encode())
        # elif "Lsensor" in command:
        #     angle_data, load_data = generate_level_data()
        #     sock.send(angle_data.encode())
        #     sock.send(load_data.encode())


def generate_level_data():
    # simulate inclinometer
    num1 = random.random()
    num2 = random.random()
    angle_data = "L-D-1,{:.2f},{:.2f}\n".format(num1, num2)
    print("send data: " + angle_data)
    # simulate load cells
    load_list = [str(random.randint(0, 1000)) for i in range(4)]
    load_data = "L-D-2," + ",".join(load_list) + "\n"
    return angle_data, load_data


threading.Thread(target=receive).start()