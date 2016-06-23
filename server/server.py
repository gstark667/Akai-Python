from socket import *
import threading
import json
import time
import signal
import sys
import hashlib
import binascii
import database
from OpenSSL import SSL

HOST = ""
PORT = 6667

clients = {}

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

   def searchUsers(self, message):
      found_users = database.searchUsers(message["query"])
      response = {"action":"RESP", "good":"True", "found":found_users, "reqnum":message["reqnum"]}
      conn.send(json.dumps(response).encode("utf-8"))

   def handleMessage(self, message):
      message = json.loads(message)
      if message["action"] == "RESP" and message["reqnum"] in self.response_handlers:
         self.response_handlers[message["reqnum"]](message)
         del self.response_handlers[message["reqnum"]]
      if message["action"] == "SEND":
         self.distributeMessage(message)
      if message["action"] == "SEARCH":
         self.searchUsers(message)

   def distributeMessage(self, message):
      request = {"action":"RECV", "sender":self.username, "message":message["message"], "chat":message["chat"], "reqnum":"0"}
      print("distributing message")
      for receiver in message["participants"]:
         print(receiver)
         #TODO probably want to make a semaphore and lock the socket object
         if receiver in clients:
            clients[receiver].conn.send(json.dumps(request).encode("utf-8"))

   def process_messages(self):
      while True:
         try:
            data = self.conn.recv(1024)
            if len(data) == 0:
               break
            self.handleMessage(data.decode("utf-8"))
         except:
            break

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

ctx = SSL.Context(SSL.TLSv1_2_METHOD)
ctx.set_options(SSL.OP_NO_SSLv2)
ctx.use_privatekey_file("server.key")
ctx.use_certificate_file("server.crt")
ctx.load_verify_locations("server.crt")

server = SSL.Connection(ctx, socket(AF_INET, SOCK_STREAM))
server.bind((HOST, PORT))
server.listen(3)

while True:
   try:
      conn, addr = server.accept()
      client = ClientConnection(conn, addr)
      if client.is_connected:
         clients[client.username] = client
   except SSL.Error:
      print("Client failed SSL connection")
