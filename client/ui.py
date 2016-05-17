import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QApplication, QSplitter, QFrame, QTextEdit, QHBoxLayout, QListWidget, QScrollArea, QListWidgetItem, QVBoxLayout, QLabel, QGridLayout, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import config

class UI():
   def __init__(self):
      self.app = QApplication(sys.argv)

      self.username = config.user["username"]
      self.login_window = LoginWindow()
      #TODO have the login ui handle the authentication (through network.py)
      #     then have ui emit a logged in signal
      #     use that signal to initialize the mainwindow
      self.login_window.login_button.clicked.connect(self.closeLogin)
      #self.main_window = MainWindow(self.username)
      self.app.exec_()

   def closeLogin(self):
      self.login_window.close()

class LoginWindow(QWidget):
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
      self.grid.addWidget(self.login_button)

      self.show()

class MainWindow(QWidget):
   def __init__(self, username):
      super().__init__()

      self.username = username
      self.messages = {}
      self.send_on_enter = True

      self.initUI()
      #TODO create config class and load friends list from config file
      self.addFriend("octalus")

   def initUI(self):
      self.hbox = QHBoxLayout(self)

      self.friend_list = QListWidget()
      self.friend_list.itemClicked.connect(self.friendClicked)

      self.message_history = QVBoxLayout()
      self.message_history.setSpacing(0)
      self.message_history.setContentsMargins(0,0,0,0)
      self.message_history.insertStretch(-1, 1)
      self.message_history_container = QWidget()
      self.message_history_container.setLayout(self.message_history)
      self.message_scroll = QScrollArea()
      self.message_scroll.setWidget(self.message_history_container)
      self.message_scroll.setWidgetResizable(True)

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
      self.messages[username] = []
      self.messages[username].append(("octalus", "hello"))
      self.messages[username].append(("gstark", "hi"))
      #TODO we should probably sanatize these to prevent directory manipulation
      friend = QListWidgetItem(QIcon(config.ICON_DIR + username + ".png"), username)
      self.friend_list.addItem(friend)

   def friendClicked(self, item):
      print(str(item.text()))
      self.loadMessages(str(item.text()))

   def loadMessages(self, username):
      self.clearMessages()
      #TODO make the message history look pretty
      for message in self.messages[username]:
         self.recvMessage(message)

   def clearMessages(self):
      while not self.message_history.isEmpty():
         self.message_history.takeAt(0)

   def sendMessage(self):
      message = self.message_input.toPlainText().strip()
      print("Sending: %s" % (message))
      self.message_input.setText("")
      self.recvMessage((self.username, message))

   def recvMessage(self, message):
      #TODO add a timestamp to messages, maybe use a dict?
      self.message_history.addWidget(QLabel(message[0] + ':' + message[1]))
      #TODO get the scroll area to scroll to bottom when updated
      #TODO let the user pick if the scrollbar moves to the bottom when updated
      #     also have an option for now scrolling when scrolled back in history
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
