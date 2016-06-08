#TODO reorganize
#TODO add encryption
import socket
#from socket import *
import threading
import json
import time
import select
import PyQt5.QtCore
from PyQt5.QtCore import QObject
from OpenSSL import SSL

class ClientSocket(QObject):
   recv_message = PyQt5.QtCore.pyqtSignal(str, dict)
   authenticate_success = PyQt5.QtCore.pyqtSignal()
   authenticate_failure = PyQt5.QtCore.pyqtSignal()
   account_create_success = PyQt5.QtCore.pyqtSignal()
   account_create_failure = PyQt5.QtCore.pyqtSignal(str)
   recv_user_search = PyQt5.QtCore.pyqtSignal(list)

   def __init__(self, address, port):
      super().__init__()
      self.address = address
      self.port = port
      self.messages = []
      self.request_number = 0
      self.response_handlers = {}
      self.authenticated = False
      self.connected = False

      #self.connectDirect(address, port)
      #self.authenticateUser()

   def startProcessingThread(self):
      self.processing_thread = threading.Thread(target=self.processMessages)
      self.processing_thread.deamon = True
      self.processing_thread.start()

   def verifyCB(self, conn, cert, errnum, depth, ok):
      print("Got Cert: %s" % cert.get_subject())
      self.ssl_started = ok
      return ok

   def connectDirect(self, address, port):
      ctx = SSL.Context(SSL.TLSv1_2_METHOD)
      ctx.set_verify(SSL.VERIFY_PEER, self.verifyCB)
      ctx.use_privatekey_file("/home/octalus/client.key")
      ctx.load_verify_locations('/home/octalus/server.crt')

      self.sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
      #self.sock.settimeout(1)
      self.sock.connect((address, port))
      self.connected = True
      #self.sock.send(b"")
      #print(self.sock.recv(128))
      #self.startProcessingThread()

   def disconnect(self):
      self.connected = False
      self.sock.close()

   def checkAuthentication(self, response):
      print("Checking Authentication")
      if response["good"] == "True":
         print("User Authenticated")
         self.authenticated = True
         self.authenticate_success.emit()
      else:
         print("Authentication Failed")
         self.authenticated = False
         self.authenticate_failure.emit()

   def checkAccountCreation(self, response):
      print("Checking Account Creation")
      if response["good"] == "True":
         self.authenticated = True
         self.account_create_success.emit()
      else:
         print("Account Creation Failed")
         print(response["message"])
         self.authenticated = False
         self.account_create_failure.emit(response["message"])

   def authenticateUser(self, username, password):
      self.connectDirect(self.address, self.port)
      self.username = username
      self.password = password
      request = {"action":"AUTH", "username":username, "password":password,
                 "reqnum":self.request_number}
      self.response_handlers[self.request_number] = self.checkAuthentication
      self.sendRequest(json.dumps(request))
      self.startProcessingThread()

   def incrementRequestNumber(self):
      self.request_number = (self.request_number + 1) % 256

   def sendResponse(self, response):
      self.sock.send(json.dumps(response).encode("utf-8"))

   def sendRequest(self, request):
      self.sock.send(request.encode("utf-8"))
      self.incrementRequestNumber()

   def sendMessage(self, message, chat, participants):
      #TODO setup a response callback
      while not self.authenticated:
         time.sleep(1)
      request = {"action": "SEND", "message": message, "chat": chat, "participants": participants}
      self.sendRequest(json.dumps(request))

   def receiveMessage(self, request):
      print("%s:%s" % (request["sender"], request["message"]))
      response = {"action":"RESP", "good":"True", "reqnum":request["reqnum"]}
      #sendResponse(response)
      self.recv_message.emit(request["chat"], {"sender":request["sender"], "message":request["message"]})
      #self.ui_recv_message_callback(request["chat"], {"sender":request["sender"], "message":request["message"]})

   def handleMessage(self, message):
      print(message)
      message = json.loads(message)
      if message["action"] == "RESP" and message["reqnum"] in self.response_handlers:
         self.response_handlers[message["reqnum"]](message)
         del self.response_handlers[message["reqnum"]]
      elif message["action"] == "RECV":
         self.receiveMessage(message)

   def processMessages(self):
      #TODO make sure all socket operations are try catched
      #TODO might want to use select instead of a bunch of timeouts
      while self.connected:
         try:
            readable, writable, exception = select.select([self.sock], [], [self.sock], 1)
            print(readable)
            print(writable)
            print(exception)
            if readable:
               data = self.sock.recv(256)
               if len(data) == 0:
                  break
               self.handleMessage(data.decode("utf-8"))
         except socket.timeout:
            continue
         except socket.error:
            break

   def createAccount(self, username, password, email):
      self.connectDirect(self.address, self.port)
      self.username = username
      self.password = password
      self.email    = email
      request = {"action":"CREATE", "username":username, "password":password, "email":email, "reqnum":self.request_number}
      self.response_handlers[self.request_number] = self.checkAccountCreation
      self.sendRequest(json.dumps(request))

   def searchUser(self, query):
      request = {"action":"SEARCH", "query":query, "reqnum":self.request_number}
      self.response_handlers[self.request_number] = self.recvUserSearch
      self.sendRequest(json.dumps(request))

   def recvUserSearch(self, response):
      self.recv_user_search.emit(response["found"])
