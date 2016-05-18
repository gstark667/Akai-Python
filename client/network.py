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

      self.connectDirect(address, port)
      #self.authenticateUser()

      self.processing_thread = threading.Thread(target=self.processMessages)
      self.processing_thread.deamon = True
      self.processing_thread.start()

   def connectDirect(self, address, port):
      self.sock = socket(AF_INET, SOCK_STREAM)
      self.sock.connect((address, port))

   def disconnect(self):
      self.sock.close()

   def checkAuthentication(self, response):
      print("Checking Authentication")
      if response["good"] == "True":
         print("User Authenticated")
         self.authenticated = True
      else:
         print("Authentication Failed")
         self.authenticated = False
         self.disconnect()

   def checkAccountCreation(self, response):
      print("Checking Account Creation")
      if response["good"] == "True":
         self.authenticated = True
      else:
         print("Account Creation Failed")
         print(response["message"])
         self.authenticated = False
         self.disconnect()

   def authenticateUser(self):
      request = {"action":"AUTH", "username":self.username, "password":self.password,
                 "reqnum":self.request_number}
      self.response_handlers[self.request_number] = self.checkAuthentication
      self.sendRequest(json.dumps(request))

   def incrementRequestNumber(self):
      self.request_number = (self.request_number + 1) % 256

   def sendResponse(self, response):
      self.sock.send(json.dumps(response).encode("utf-8"))

   def sendRequest(self, request):
      self.sock.send(request.encode("utf-8"))
      self.incrementRequestNumber()

   def sendMessage(self, message, recipiant):
      while not self.authenticated:
         time.sleep(1)
      request = {"action": "SEND", "recipiant": recipiant, "content": message}
      self.sendRequest(json.dumps(request))

   def receiveMessage(self, request):
      print("%s:%s" % (request["sender"], request["content"]))
      response = {"action":"RESP", "good":"True", "reqnum":request["reqnum"]}
      sendResponse(response)

   def handleMessage(self, message):
      message = json.loads(message)
      if message["action"] == "RESP" and message["reqnum"] in self.response_handlers:
         self.response_handlers[message["reqnum"]](message)
         del self.response_handlers[message["reqnum"]]
      elif message["action"] == "RECV":
         self.receiveMessage(message)

   def processMessages(self):
      while True:
         data = self.sock.recv(1024)
         if len(data) == 0:
            break
         self.handleMessage(data.decode("utf-8"))

   def createUser(self):
      request = {"action":"CREATE", "username":"octalus", "password":"something", "email":"something", "reqnum":self.request_number}
      self.response_handlers[self.request_number] = self.checkAccountCreation
      self.sendRequest(json.dumps(request))
      

socket = ClientSocket("localhost", 6667, "gstark", "potato")
socket.createUser()
socket.sendMessage("Hello", "gstark")
