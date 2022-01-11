import socket
import threading
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.8.154", 8080)
sock.connect(server_address)
sock.send("IDlevel".encode())


def receive():
    while True:
        data = sock.recv(1024).decode()
        if data.startswith("Lsensor"):
            # simulate inclinometer
            num1 = random.random()
            num2 = random.random()
            angle_data = "LD1,{:.2f},{:.2f}\n".format(num1, num2)
            sock.send(angle_data.encode())
            print("send data: " + angle_data)
            # simulate load cells
            load_list = [str(random.randint(0, 1000)) for i in range(4)]
            load_data = "LD2," + ",".join(load_list) + "\n"
            sock.send(load_data.encode())

        elif data.startswith("L"):
            print(data)


threading.Thread(target=receive).start()
