#TODO reorganize
#TODO add encryption
import socket
#from socket import *
import threading
import json
import time
import select

class ClientSocket:
   def __init__(self, address, port):
      self.address = address
      self.port = port
      self.messages = []
      self.request_number = 0
      self.response_handlers = {}
      self.authenticated = False

      #self.connectDirect(address, port)
      #self.authenticateUser()

   def startProcessingThread(self):
      self.processing_thread = threading.Thread(target=self.processMessages)
      self.processing_thread.deamon = True
      self.processing_thread.start()

   def connectDirect(self, address, port):
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.settimeout(1)
      self.sock.connect((address, port))
      self.startProcessingThread()

   def disconnect(self):
      self.sock.close()

   def checkAuthentication(self, response):
      print("Checking Authentication")
      if response["good"] == "True":
         print("User Authenticated")
         self.authenticated = True
         self.authenticate_success_callback()
      else:
         print("Authentication Failed")
         self.authenticated = False
         self.authenticate_failure_callback()

   def checkAccountCreation(self, response):
      print("Checking Account Creation")
      if response["good"] == "True":
         self.authenticated = True
         self.creation_success_callback()
      else:
         print("Account Creation Failed")
         print(response["message"])
         self.authenticated = False
         self.creation_failure_callback(response["message"])

   def authenticateUser(self, username, password):
      self.connectDirect(self.address, self.port)
      self.username = username
      self.password = password
      self.authenticate_success_callback = authenticate_success_callback
      self.authenticate_failure_callback = authenticate_failure_callback
      request = {"action":"AUTH", "username":username, "password":password,
                 "reqnum":self.request_number}
      self.response_handlers[self.request_number] = self.checkAuthentication
      self.sendRequest(json.dumps(request))

   def authenticateUser(self, username, password, authenticate_success_callback, authenticate_failure_callback):
      self.connectDirect(self.address, self.port)
      self.username = username
      self.password = password
      self.authenticate_success_callback = authenticate_success_callback
      self.authenticate_failure_callback = authenticate_failure_callback
      request = {"action":"AUTH", "username":username, "password":password,
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
      #TODO make sure all socket operations are try catched
      #TODO might want to use select instead of a bunch of timeouts
      while True:
         try:
            data = self.sock.recv(1024)
            if len(data) == 0:
               break
            self.handleMessage(data.decode("utf-8"))
         except socket.timeout:
            continue
         except socket.error:
            break

   def createAccount(self, username, password, email, creation_success_callback, creation_failure_callback):
      self.connectDirect(self.address, self.port)
      self.username = username
      self.password = password
      self.email    = email
      self.creation_success_callback = creation_success_callback
      self.creation_failure_callback = creation_failure_callback
      request = {"action":"CREATE", "username":username, "password":password, "email":email, "reqnum":self.request_number}
      self.response_handlers[self.request_number] = self.checkAccountCreation
      self.sendRequest(json.dumps(request))
