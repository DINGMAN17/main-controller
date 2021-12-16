import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server given by the caller
#server_address = ('192.168.1.3', 12345)
server_address = ('127.0.0.1', 12345)

sock.connect(server_address)

message = input()
while message != "quit":
    print("sending message: " + message)
    sock.send(message.encode())
    message = input()
