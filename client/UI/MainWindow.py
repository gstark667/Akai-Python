import config
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, \
   QMainWindow, QScrollArea, QSplitter, QTextEdit, QVBoxLayout, QWidget
from UI.Dialog import CreateChatDialog

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
      print(config.chats)
      for chat in config.chats:
         self.createChat(chat, config.chats[chat]["participants"])

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

   def createChat(self, chat_name=None, participants=None):
      if chat_name == None or participants == None:
         create_chat_dialog = CreateChatDialog()
         create_chat_dialog.exec_()
         if not create_chat_dialog.created_chat:
            return
         chat_name = create_chat_dialog.chat_name
         participants = create_chat_dialog.participants
      self.chats[chat_name] = {"participants":participants, "messages":[]}
      self.friend_list.addItem(QListWidgetItem(chat_name))

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

   def disconnect(self):
      self.client_socket.disconnect()

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
