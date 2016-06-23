import pyaudio
import socket
import sys
import threading


frames = []


def udp_stream(CHUNK):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 5001))
    while True:
        if len(frames) > 0:
            data = sock.sendto(frames.pop(0), ('localhost', 5000))
    sock.close()


def record(stream, CHUNK):
    while True:
        frames.append(stream.read(CHUNK))


FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True)

threading.Thread(target=udp_stream, args=[CHUNK]).start()
threading.Thread(target=record, args=[stream, CHUNK]).start()

#s.close()
#stream.close()
#p.terminate()
