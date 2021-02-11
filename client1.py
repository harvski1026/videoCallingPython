from multiprocessing import Process
import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import socket
import pyaudio
import wave


def video_stream():
    cap = cv2.VideoCapture(0)
    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('192.168.1.11', 50053))
    except socket.error as exc:
        print("")

    while True:
        ret, frame = cap.read()
        data = pickle.dumps(frame)
        clientsocket.sendall(struct.pack("L", len(data)) + data)


def audio_stream():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 40

    try:
        HOST = '192.168.1.11'  # The remote host
        PORT = 8000  # The same port as used by the server

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
    except socket.error as exc:
        print("")




    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("*recording")

    frames = []

    while True:
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            s.sendall(data)

        print("*done recording")

        # stream.stop_stream()
        # stream.close()
        # p.terminate()
        # s.close()

        print("*closed")


if __name__ == '__main__':
    v_stream = Process(target=video_stream)
    a_stream = Process(target=audio_stream)
    v_stream.start()
    a_stream.start()
