from socket import *
import threading
import json
import time
import signal
import sys
import hashlib
import binascii

HOST = ""
PORT = 4242

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

def handle_request(username, request):
   if request["action"] == "SEND":
      send_request = {"action": "RECV", "sender": username, "content": request["content"]}
      clients[request["recipiant"]][0].send(json.dumps(send_request).encode("utf-8"))

def handle_message(username, message):
   request = json.loads(message)
   handle_request(username, request)

def handle_client(conn, addr):
   conn.send(b'{"action": "AUTH"}')

   responses = []
   username = ""
   while True:
      data = conn.recv(1024)
      response = json.loads(data.decode("utf-8"))
      if response["action"] == "AUTH":
         username = response["username"]
         break
      else:
         responses.append(response)

   print(authenticate(username, response["password"]))
      
   clients[username] = (conn, addr)
   print("Accepted Client:%s" % (username))

   for response in responses:
      handle_request(username, response)

   while True:
      data = conn.recv(1024)
      if len(data) == 0:
         break
      handle_message(username, data.decode("utf-8"))

   print("Client Disconnected")
   conn.close()

def signal_handler(signal, frame):
   global server
   print("Shutting Down Server")
   server.close()
   for client in clients:
      clients[client][0].close()
   sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

server = socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

while True:
   conn, addr = server.accept()
   tmp = threading.Thread(target=handle_client, args=[conn, addr])
   tmp.deamon = True
   tmp.start()
