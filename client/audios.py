import pyaudio
import socket
import sys
import threading


frames = []


FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 2
RATE = 44100


def udp_stream():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 5000))
    while True:
        data, addr = sock.recvfrom(CHUNK * CHANNELS * 2)
        frames.append(data)
    sock.close()


def play(stream):
    while True:
        if len(frames) > 10:
            for i in range(0, len(frames)):
                stream.write(frames.pop(0), CHUNK)


p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True)

stream.start_stream()

threading.Thread(target=udp_stream).start()
threading.Thread(target=play, args=[stream]).start()

#s.close()
#stream.close()
#p.terminate()
