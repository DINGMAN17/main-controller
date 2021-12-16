#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import numpy as np
import socket, cv2, pickle, struct

IP_SERVER = "192.168.1.3"
PORT_SERVER = 12344
TIMEOUT_SOCKET = 10
SIZE_PACKAGE = 4096

IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640
COLOR_PIXEL = 3  # RGB

data = b""
payload_size = struct.calcsize("Q")

if __name__ == '__main__':
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.settimeout(TIMEOUT_SOCKET)
    connection.connect((IP_SERVER, PORT_SERVER))

    while True:
        try:
            while len(data) < payload_size:
                packet = connection.recv(4 * 1024)  # 4K
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += connection.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("RECEIVING VIDEO2", frame)
            if cv2.waitKey(1) == '13':
                break


            # fileDescriptor = connection.makefile(mode='rb')
            # result = fileDescriptor.readline()
            # fileDescriptor.close()
            # result = base64.b64decode(result)
            #
            # frame = np.fromstring(result, dtype=np.uint8)
            # frame_matrix = np.array(frame)
            # frame_matrix = np.reshape(frame_matrix, (IMAGE_HEIGHT, IMAGE_WIDTH,
            #                                          COLOR_PIXEL))
            # cv2.imshow('Window title', frame_matrix)

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        except Exception as e:
            print ("[Error] " + str(e))

    connection.close()
