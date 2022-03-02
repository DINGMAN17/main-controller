import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.8.154", 8080)
sock.connect(server_address)
sock.send("IDadmin".encode())

expected_result = ("L-STATUS-ready", "M-STATUS-ready")


def receive():
    status_count = 0
    results = []
    while status_count <= 1:
        command = sock.recv(1024).decode().strip()
        print(command)
        results.append(command)
        status_count += 1
    assert sorted(results) == sorted(expected_result)


receive()
