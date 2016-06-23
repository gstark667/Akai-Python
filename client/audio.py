import pyaudio
import socket
import sys
import threading


output_frames = []
input_frames = []
port = int(sys.argv[1])
peer_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', port))

#TODO merge the stream methods into one big one with a select statement
def udp_stream_input():
    while True:
        if len(input_frames) > 0:
            data = sock.sendto(input_frames.pop(0), ('localhost', peer_port))


def udp_stream_output():
    while True:
        data, addr = sock.recvfrom(CHUNK * CHANNELS * 2)
        output_frames.append(data)


def play(stream):
    while True:
        if len(output_frames) > 10:
            for i in range(0, len(output_frames)):
                stream.write(output_frames.pop(0), CHUNK)


def record(stream):
    while True:
        input_frames.append(stream.read(CHUNK))


FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

input_stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True)
output_stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True)


threading.Thread(target=udp_stream_input).start()
threading.Thread(target=udp_stream_output).start()
threading.Thread(target=record, args=[input_stream]).start()
threading.Thread(target=play, args=[output_stream]).start()

#s.close()
#stream.close()
#p.terminate()
