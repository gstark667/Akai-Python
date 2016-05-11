from socket import *
import threading
import json
import time

class ClientSocket:
   def __init__(self, address, port, username, password):
      self.connect_direct(address, port)
      self.username = username
      self.password = password
      self.messages = []
      self.processing_thread = threading.Thread(target=self.process_messages)
      self.processing_thread.deamon = True
      self.processing_thread.start()
      self.request_number = 0

   def increment_request_number(self):
      self.request_number = (self.request_number + 1) % 256

   def connect_direct(self, address, port):
      self.sock = socket(AF_INET, SOCK_STREAM)
      self.sock.connect((address, port))

   def send_request(self, request):
      self.sock.send(request.encode("utf-8"))

   def send_message(self, message, recipiant):
      request = {"action": "SEND", "recipiant": recipiant, "content": message}
      self.send_request(json.dumps(request))

   def handle_message(self, message):
      request = json.loads(message)
      if request["action"] == "AUTH":
         response = {"action": "AUTH", "username": self.username,
                     "password": self.password, "request": self.request_number}
         self.increment_request_number()
         self.send_request(json.dumps(response))
      elif request["action"] == "RECV":
         print("%s:%s" % (request["sender"], request["content"]))

   def process_messages(self):
      while True:
         data = self.sock.recv(1024)
         if len(data) == 0:
            break
         self.handle_message(data.decode("utf-8"))

socket = ClientSocket("localhost", 4242, "gstark", "potato")
socket.send_message("Hello", "gstark")

time.sleep(100);
