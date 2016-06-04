#TODO implement i18n eventually
import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QApplication, QSplitter, QFrame, QTextEdit, QHBoxLayout, QListWidget, QScrollArea, QListWidgetItem, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QDialog, QMainWindow, QAction
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import config, network
import time

class UI():
   def __init__(self):
      self.app = QApplication(sys.argv)

      if "username" in config.user and "password" in config.user:
         self.finished_auto = False
         self.autoLogin()
      else:
         self.createLogin()

   def autoLogin(self):
      self.client_socket = network.ClientSocket("localhost", 6667)
      self.client_socket.authenticateUser(config.user["username"], config.user["password"])
      self.client_socket.authenticate_success.connect(self.createMain)
      self.client_socket.authenticate_failure.connect(self.createLogin)

   def autoLoginSuccess(self):
      self.finished_auto = True
      self.auto_success  = True

   def autoLoginFailure(self):
      self.finished_auto = True
      self.auto_success  = False

   def createLogin(self):
      self.login_window = LoginWindow()
      self.login_window.loggedIn.connect(self.finishLogin)
      self.login_window.exit.connect(self.closeApplication)

   def finishLogin(self):
      self.login_window.close()
      self.client_socket = self.login_window.client_socket
      self.createMain()

   def createMain(self):
      self.main_window = MainWindow(self.client_socket, self.app.processEvents)

   def closeApplication(self):
      self.app.quit()

   def exec(self):
      return self.app.exec_()

class LoginWindow(QWidget):
   loggedIn = pyqtSignal()
   exit     = pyqtSignal()
   
   def __init__(self):
      super().__init__()
      self.initUI()

   def initUI(self):
      self.grid = QGridLayout(self)

      self.username_label = QLabel("Username:")
      self.grid.addWidget(self.username_label, 0, 0, 1, 1)
      self.username_field = QLineEdit()
      self.grid.addWidget(self.username_field, 0, 1, 1, 1)

      self.password_label = QLabel("Password:")
      self.grid.addWidget(self.password_label, 1, 0, 1, 1)
      self.password_field = QLineEdit()
      self.password_field.setEchoMode(QLineEdit.Password)
      self.grid.addWidget(self.password_field, 1, 1, 1, 1)

      self.login_button = QPushButton("Login")
      self.login_button.pressed.connect(self.login)
      self.grid.addWidget(self.login_button, 2, 0, 1, 2)

      self.create_button = QPushButton("Create Account")
      self.create_button.pressed.connect(self.createUser)
      self.grid.addWidget(self.create_button, 3, 0, 1, 2)
      #TODO add account recovery
      #TODO add options button for language and server config

      self.exit_button = QPushButton("Exit")
      self.exit_button.pressed.connect(self.exitLogin)
      self.grid.addWidget(self.exit_button, 4, 0, 1, 2)

      self.show()

   def login(self):
      self.client_socket = network.ClientSocket("localhost", 6667)
      self.client_socket.authenticateUser(self.username_field.text(), self.password_field.text())
      self.client_socket.authenticate_success.connect(self.loginSuccess)
      self.client_socket.authenticate_failure.connect(self.loginFailure)

   def loginSuccess(self):
      config.user["username"] = self.username_field.text()
      config.user["password"] = self.password_field.text()
      self.loggedIn.emit()

   def loginFailure(self):
      print("Failed to authenticate against server")

   def createUser(self):
      create_account_dialog = CreateAccountDialog()
      create_account_dialog.exec_()
      self.client_socket = create_account_dialog.client_socket
      self.loginSuccess()

   def exitLogin(self):
      self.exit.emit()

class CreateAccountDialog(QDialog):
   def __init__(self):
      super().__init__()
      self.initUI()
      self.created_account = False

   def initUI(self):
      self.setWindowModality(Qt.ApplicationModal)
      self.setWindowTitle("Create Account")

      self.grid = QGridLayout(self)

      self.username_label = QLabel("Username:")
      self.grid.addWidget(self.username_label, 0, 0, 1, 1)
      self.username_field = QLineEdit()
      self.grid.addWidget(self.username_field, 0, 1, 1, 1)

      self.email_label = QLabel("Email:")
      self.grid.addWidget(self.email_label, 1, 0, 1, 1)
      self.email_field = QLineEdit()
      self.grid.addWidget(self.email_field, 1, 1, 1, 1)

      self.password_label = QLabel("Password:")
      self.grid.addWidget(self.password_label, 2, 0, 1, 1)
      self.password_field = QLineEdit()
      self.password_field.setEchoMode(QLineEdit.Password)
      self.grid.addWidget(self.password_field, 2, 1, 1, 1)

      self.password_confirm_label = QLabel("Password Confirm:")
      self.grid.addWidget(self.password_confirm_label, 3, 0, 1, 1)
      self.password_confirm_field = QLineEdit()
      self.password_confirm_field.setEchoMode(QLineEdit.Password)
      self.grid.addWidget(self.password_confirm_field, 3, 1, 1, 1)

      self.create_button = QPushButton("Create")
      self.create_button.pressed.connect(self.createAccount)
      self.grid.addWidget(self.create_button, 4, 0, 1, 2)

      self.cancel_button = QPushButton("Cancel")
      self.cancel_button.pressed.connect(self.cancel)
      self.grid.addWidget(self.cancel_button, 5, 0, 1, 2)

   def createAccount(self):
      #TODO add some sort of error message to the ui
      username = self.username_field.text()
      email    = self.email_field.text()
      password = self.password_field.text()
      password_confirm = self.password_confirm_field.text()
      if len(username) == 0:
         print("username cannot be empty")
         return

      if len(email) == 0:
         print("email cannot be empty")
         return

      if len(password) == 0:
         print("password cannot be empty")
         return

      if not password == password_confirm:
         print("passwords do not match")
         return

      self.client_socket = network.ClientSocket("localhost", 6667)
      self.client_socket.createAccount(self.username_field.text(), self.password_field.text(), self.email_field.text())
      self.client_socket.account_create_success.connect(self.createAccountSuccess)
      self.client_socket.account_create_failure.connect(self.createAccountFailure)

   def createAccountSuccess(self):
      config.user["username"] = self.username_field.text()
      config.user["password"] = self.password_field.text()
      self.created_account = True
      self.close()

   def createAccountFailure(self, message):
      print(message)

   def cancel(self):
      self.created_account = False
      self.close()

class MainWindow(QMainWindow):
   def __init__(self, client_socket, process_events_method):
      super().__init__()

      self.username = config.user["username"]
      self.client_socket = client_socket
      self.client_socket.recv_message.connect(self.recvMessage)
      self.process_events_method = process_events_method
      self.chats = {}
      self.send_on_enter = True

      self.initMenubar()
      self.initUI()
      #TODO load friends list from config file
      self.addFriend("test")
      self.addFriend("octalus")
      for i in range(100):
         self.chats["octalus"]["messages"].append({"sender":"test", "message":"hello"})

   def initMenubar(self):
      self.exitAction = QAction("&Create Chat", self)
      #self.exitAction.setShortcut("Ctrl+Q")
      self.exitAction.triggered.connect(self.createChat)

      self.menubar = self.menuBar()
      self.fileMenu = self.menubar.addMenu("&Chat")
      self.fileMenu.addAction(self.exitAction)

   def initUI(self):
      self.content = QWidget()

      self.hbox = QHBoxLayout(self.content)
      self.setCentralWidget(self.content)

      self.friend_list = QListWidget()
      self.friend_list.itemClicked.connect(self.friendClicked)

      self.message_scroll = QScrollArea()
      self.message_scroll.setWidgetResizable(True)
      #TODO have a setting to disable this
      self.message_scroll.verticalScrollBar().rangeChanged.connect(self.scrollBottom)

      self.message_input = MessageInput()
      self.message_input.sendMessage.connect(self.sendMessage)

      self.message_split = QSplitter(Qt.Vertical)
      self.message_split.addWidget(self.message_scroll)
      self.message_split.addWidget(self.message_input)

      self.main_split = QSplitter(Qt.Horizontal)
      self.main_split.addWidget(self.friend_list)
      self.main_split.addWidget(self.message_split)

      self.hbox.addWidget(self.main_split)

      self.show()

   def addFriend(self, username):
      #TODO load message history here
      self.chats[username] = {"participants":[username], "messages":[]}
      #TODO we should probably sanatize these to prevent directory manipulation
      friend = QListWidgetItem(QIcon(config.ICON_DIR + username + ".png"), username)
      self.friend_list.addItem(friend)

   def createChat(self):
      create_chat_dialog = CreateChatDialog()
      create_chat_dialog.exec_()
      #self.chats[chat] = {"participants":participants, "message":[]}
      #self.friend_list.addItem(chat)

   def friendClicked(self, item):
      self.loadMessages(str(item.text()))

   def loadMessages(self, chat):
      #self.clearMessages()
      #TODO make the message history look pretty
      #TODO consider storing a message history for each chat and switch between when needed
      #TODO create a chat class and store the chat name as well as the participants there
      #TODO index message histories by chat name
      self.message_history = QVBoxLayout()
      self.message_history.setSpacing(0)
      self.message_history.setContentsMargins(0,0,0,0)
      self.message_history.insertStretch(-1, 1)
      self.message_history_container = QWidget()
      self.message_history_container.setLayout(self.message_history)
      self.message_scroll.setWidget(self.message_history_container)
      for message in self.chats[chat]["messages"]:
         self.drawMessage(message)

   def clearMessages(self):
      while not self.message_history.isEmpty():
         self.message_history.takeAt(0)

   def sendMessage(self):
      message = self.message_input.toPlainText().strip()
      chat = self.friend_list.selectedItems()[0].text()
      self.client_socket.sendMessage(message, chat, self.chats[chat]["participants"])
      print("Sending: %s to %s" % (message, chat))
      self.message_input.setText("")
      self.recvMessage(chat, {"sender":self.username, "message":message})

   def recvMessage(self, chat, message):
      self.chats[chat]["messages"].append(message)
      current_chat = self.friend_list.selectedItems()[0].text()
      if current_chat == chat:
         self.drawMessage(message)

   def drawMessage(self, message):
      #TODO add a timestamp to messages
      new_message = QLabel(message["sender"] + ':' + message["message"])
      self.message_history.addWidget(new_message)

   def scrollBottom(self):
      self.message_scroll.verticalScrollBar().setValue(self.message_scroll.verticalScrollBar().maximum())
      
class MessageInput(QTextEdit):
   sendMessage = pyqtSignal()

   def __init__(self):
      super().__init__()
      self.can_send_message = True

   def keyPressEvent(self, event):
      super().keyPressEvent(event)
      if event.key() == Qt.Key_Shift:
         self.can_send_message = False
      elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
         if self.can_send_message:
            self.sendMessage.emit()

   def keyReleaseEvent(self, event):
      super().keyPressEvent(event)
      if event.key() == Qt.Key_Shift:
         self.can_send_message = True

class CreateChatDialog(QDialog):
   def __init__(self):
      super().__init__()
      self.initUI()

   def initUI(self):
      self.setWindowModality(Qt.ApplicationModal)
      self.setWindowTitle("Create Chat")

      self.grid = QGridLayout(self)

      self.chat_name_label = QLabel("Chat Name:")
      self.grid.addWidget(self.username_label, 0, 0, 1, 1)
      self.chat_name_field = QLineEdit()
      self.grid.addWidget(self.username_field, 0, 1, 1, 2)

      #TODO make this actually about chats
      self.email_label = QLabel("Email:")
      self.grid.addWidget(self.email_label, 1, 0, 1, 1)
      self.email_field = QLineEdit()
      self.grid.addWidget(self.email_field, 1, 1, 1, 1)

      self.password_label = QLabel("Password:")
      self.grid.addWidget(self.password_label, 2, 0, 1, 1)
      self.password_field = QLineEdit()
      self.password_field.setEchoMode(QLineEdit.Password)
      self.grid.addWidget(self.password_field, 2, 1, 1, 1)

      self.password_confirm_label = QLabel("Password Confirm:")
      self.grid.addWidget(self.password_confirm_label, 3, 0, 1, 1)
      self.password_confirm_field = QLineEdit()
      self.password_confirm_field.setEchoMode(QLineEdit.Password)
      self.grid.addWidget(self.password_confirm_field, 3, 1, 1, 1)

#class OptionsDialog(QDialog):
#   def __init__(self):
