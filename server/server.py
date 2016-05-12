from socket import *
import threading
import json
import time
import signal
import sys
import hashlib
import binascii

HOST = ""
PORT = 6667

clients = {}
#this is for testing
#password is potato
#hash was generated with os.urandom(32)
users = {"gstark": (b"990152d7bfce354f7d720d5859ff7f6ea88a52d1e78ff2c9e63297a298a25e5f",
                     b"11b1a017c76c6f4fcabc498b344ca11c88e0cda7ad8a896f03af0907220f0100")}

def authenticate(username, password):
   user = users[username]
   if not user:
      return false
   password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), user[1], 1000000)
   password_hash = binascii.hexlify(password_hash)
   return password_hash == user[0]

class ClientConnection():
   def __init__(self, conn, addr):
      self.conn = conn
      self.addr = addr

      self.is_connected = self.authenticate_client()
      if not self.is_connected:
         self.disconnect()
         return

      self.response_handlers = {}

      self.processing_thread = threading.Thread(target=self.process_messages)
      self.processing_thread.deamon = True
      self.processing_thread.start()

   def disconnect(self):
      self.conn.close()

   def authenticate_client(self):
      request = conn.recv(1024)
      request = json.loads(request.decode("utf-8"))
      if not request["action"] == "AUTH":
         return False
      if not authenticate(request["username"], request["password"]):
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
   sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

server = socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

while True:
   conn, addr = server.accept()
   client = ClientConnection(conn, addr)
   if client.is_connected:
      clients[client.username] = client
