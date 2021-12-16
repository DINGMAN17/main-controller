import cv2
import imutils
import pickle
import struct


class ClientHandler:
    def __init__(self, client_socket, address):
        self.address = address
        self.client_socket = client_socket

    def send_message(self):
        pass

    def receive_message(self):
        # try to receive data from the client
        while True:
            data = self.client_socket.recv(1024).decode()
            if data.startswith("msg"):
                print(data)

    def send_video(self):
        webcam = cv2.VideoCapture(0)

        while (webcam.isOpened()):
            img, frame = webcam.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            self.client_socket.sendall(message)

            cv2.imshow('TRANSMITTING VIDEO', frame)
            if cv2.waitKey(1) == '13':
                self.client_socket.close()
