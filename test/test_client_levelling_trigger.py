import socket
import threading
import random
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 8080)
sock.connect(server_address)
sock.send("IDlevel".encode())


def receive():
    status_list = ["L-STATUS-ready", "L-STATUS-busy", "L-STATUS-error", "L-STATUS-lock"]
    while True:
        data = sock.recv(1024).decode()
        if data.startswith("Lsensor"):
            # simulate inclinometer
            num1 = random.random()
            num2 = random.random()
            angle_data = "L-D-1,{:.2f},{:.2f}\n".format(num1, num2)
            sock.send(angle_data.encode())
            print("send data: " + angle_data)
            # simulate load cells
            load_list = [str(random.randint(0, 1000)) for i in range(4)]
            load_data = "L-D-2," + ",".join(load_list) + "\n"
            sock.send(load_data.encode())
        elif data.startswith("Lstatus"):
            status = random.choice(status_list)
            sock.send(status.encode())
            print("status: " + status)

        elif data.startswith("L"):
            print(data)


def send():
    count = 0
    while True:
        data = "L-INFO-" + str(count)
        sock.send(data.encode())
        print("send data:", data)
        count += 1
        time.sleep(10)


threading.Thread(target=receive).start()
#threading.Thread(target=send).start()
