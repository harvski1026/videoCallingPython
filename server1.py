from multiprocessing import Process
import threading
import socket
import sys
import cv2
import pickle
import numpy as np
import struct
# Echo server program
import socket
import pyaudio
import wave
import time

HOST = '192.168.1.11'
PORT = 50053


def audio_stream():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        s.bind(('192.168.1.11', 8000))
        print('Socket bind complete')
        s.listen(20)
        print('Socket now listening')

        conn__, addr_ = s.accept()

    except socket.error as exc:

        print("")

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 4
    WAVE_OUTPUT_FILENAME = "server_output.wav"
    WIDTH = 2
    frames = []

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    data_ = conn__.recv(1024)

    i = 1
    while data_ != '':
        stream.write(data_)
        data_ = conn__.recv(1024)
        i = i + 1
        print(i)
        frames.append(data_)

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    stream.stop_stream()
    stream.close()
    p.terminate()
    conn.close()


def video_stream():
    global HOST, PORT
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        s.bind((HOST, PORT))
        print('Socket bind complete')
        s.listen(20)
        print('Socket now listening')

        conn1, addr1 = s.accept()


    except socket.error as exc:
        print("")
    data = b''
    payload_size = struct.calcsize("L")
    while True:
        while len(data) < payload_size:
            data += conn1.recv(4096)
        packed_msg_size = data[:payload_size]

        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn1.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        print(frame.size)
        cv2.imshow('Client Image', frame)
        cv2.waitKey(10)


if __name__ == '__main__':
    v_stream = Process(target=video_stream)
    a_stream = Process(target=audio_stream)
    v_stream.start()
    a_stream.start()
