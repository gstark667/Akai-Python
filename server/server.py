from socket import *
import threading
import json
import time
import signal
import sys
import hashlib
import binascii
import database

HOST = ""
PORT = 6667

clients = {}
#this is for testing
#password is potato
#hash was generated with os.urandom(32)

class ClientConnection():
   def __init__(self, conn, addr):
      self.conn = conn
      self.addr = addr

      self.is_connected = self.authenticate_client()
      if not self.is_connected:
         self.disconnect()
         print("Client Authentication Failure")
         return
      print("Client Connected")

      self.response_handlers = {}

      self.processing_thread = threading.Thread(target=self.process_messages)
      self.processing_thread.deamon = True
      self.processing_thread.start()

   def disconnect(self):
      self.conn.close()

   def authenticate_client(self):
      request = conn.recv(1024)
      request = json.loads(request.decode("utf-8"))
      if request["action"] == "CREATE":
         print("Creating User")
         if request["username"] in database.users:
            response = {"action":"RESP", "good":"False", "reqnum":request["reqnum"], "message":"User already exists"}
            conn.send(json.dumps(response).encode("utf-8"))
            return False
         if len(request["username"]) == 0:
            response = {"action":"RESP", "good":"False", "reqnum":request["reqnum"], "message":"username cannot be empty"}
            conn.send(json.dumps(response).encode("utf-8"))
            return False
         if len(request["password"]) == 0:
            response = {"action":"RESP", "good":"False", "reqnum":request["reqnum"], "message":"password cannot be empty"}
            conn.send(json.dumps(response).encode("utf-8"))
            return False
         if len(request["email"]) == 0:
            response = {"action":"RESP", "good":"False", "reqnum":request["reqnum"], "message":"email cannot be empty"}
            conn.send(json.dumps(response).encode("utf-8"))
            return False
         if database.create_user(request):
            self.username=request["username"]
            response = {"action":"RESP", "good":"True", "reqnum":request["reqnum"]}
            conn.send(json.dumps(response).encode("utf-8"))
            return True
      if not request["action"] == "AUTH":
         response = {"action":"RESP", "good":"False", "reqnum":request["reqnum"]}
         conn.send(json.dumps(response).encode("utf-8"))
         return False
      if not database.authenticate(request["username"], request["password"]):
         response = {"action":"RESP", "good":"False", "reqnum":request["reqnum"]}
         conn.send(json.dumps(response).encode("utf-8"))
         return False
      self.username = request["username"]
      response = {"action":"RESP", "good":"True", "reqnum":request["reqnum"]}
      conn.send(json.dumps(response).encode("utf-8"))
      return True

   def handle_message(self, message):
      message = json.loads(message)
      if message["action"] == "RESP" and message["reqnum"] in self.response_handlers:
         self.response_handlers[message["reqnum"]](message)
         del self.response_handlers[message["reqnum"]]

   def process_messages(self):
      while True:
         data = self.conn.recv(1024)
         if len(data) == 0:
            break
         self.handle_message(data.decode("utf-8"))

def signal_handler(signal, frame):
   global server
   print("Shutting Down Server")
   server.close()
   for client in clients:
      clients[client].disconnect()
   database.save()
   sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
database.init()

server = socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

while True:
   conn, addr = server.accept()
   client = ClientConnection(conn, addr)
   if client.is_connected:
      clients[client.username] = client
