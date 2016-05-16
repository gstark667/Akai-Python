#TODO cleanup naming conventions
#TODO reorganize
from socket import *
import threading
import json
import time

class ClientSocket:
   def __init__(self, address, port, username, password):
      self.username = username
      self.password = password
      self.messages = []
      self.request_number = 0
      self.response_handlers = {}
      self.authenticated = False

      self.connect_direct(address, port)
      self.authenticate_user()

      self.processing_thread = threading.Thread(target=self.process_messages)
      self.processing_thread.deamon = True
      self.processing_thread.start()

   def connect_direct(self, address, port):
      self.sock = socket(AF_INET, SOCK_STREAM)
      self.sock.connect((address, port))

   def disconnect(self):
      self.sock.close()

   def check_authentication(self, response):
      print("Checking Authentication")
      if response["good"] == "True":
         print("User Authenticated")
         self.authenticated = True
      else:
         print("Authentication Failed")
         self.authenticated = False
         self.disconnect()

   def authenticate_user(self):
      request = {"action":"AUTH", "username":self.username, "password":self.password,
                 "reqnum":self.request_number}
      self.response_handlers[self.request_number] = self.check_authentication
      self.send_request(json.dumps(request))

   def increment_request_number(self):
      self.request_number = (self.request_number + 1) % 256

   def send_response(self, response):
      self.sock.send(json.dumps(response).encode("utf-8"))

   def send_request(self, request):
      self.sock.send(request.encode("utf-8"))
      self.increment_request_number()

   def send_message(self, message, recipiant):
      while not self.authenticated:
         time.sleep(1)
      request = {"action": "SEND", "recipiant": recipiant, "content": message}
      self.send_request(json.dumps(request))

   def receive_message(self, request):
      print("%s:%s" % (request["sender"], request["content"]))
      response = {"action":"RESP", "good":"True", "reqnum":request["reqnum"]}
      send_response(response)

   def handle_message(self, message):
      message = json.loads(message)
      if message["action"] == "RESP" and message["reqnum"] in self.response_handlers:
         self.response_handlers[message["reqnum"]](message)
         del self.response_handlers[message["reqnum"]]
      elif message["action"] == "RECV":
         self.receive_message(message)

   def process_messages(self):
      while True:
         data = self.sock.recv(1024)
         if len(data) == 0:
            break
         self.handle_message(data.decode("utf-8"))

socket = ClientSocket("localhost", 6667, "gstark", "potato")
socket.send_message("Hello", "gstark")
