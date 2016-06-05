import config
import network
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QListWidget, \
   QListWidgetItem, QPushButton

class CreateAccountDialog(QDialog):
   def __init__(self):
      super().__init__()
      self.initUI()
      self.created_account = False

   def initUI(self):
      self.setWindowModality(Qt.ApplicationModal)
      self.setWindowTitle("Create Account")

      self.grid = QGridLayout(self)

      self.warning_label = None

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

   def setWarning(self, message):
      if self.warning_label == None:
         self.warning_label = QLabel("")
         self.warning_label.setStyleSheet("QLabel { color: red; }")
         self.grid.addWidget(self.warning_label, 6, 0, 1, 2)
      self.warning_label.setText(message)

   def createAccount(self):
      username = self.username_field.text()
      email    = self.email_field.text()
      password = self.password_field.text()
      password_confirm = self.password_confirm_field.text()
      if len(username) == 0:
         self.setWarning("Username cannot be empty")
         return

      if len(email) == 0:
         self.setWarning("Email cannot be empty")
         return

      if len(password) == 0:
         self.setWarning("Password cannot be empty")
         return

      if not password == password_confirm:
         self.setWarning("Passwords do not match")
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
      #TODO implement error codes and i18n translation
      self.setWarning(message)

   def cancel(self):
      self.close()

class CreateChatDialog(QDialog):
   def __init__(self):
      super().__init__()
      self.initUI()
      self.created_chat = False
      self.participants = []
      self.chat_name = None

      for friend in config.friends:
         self.unadded_friends.addItem(QListWidgetItem(friend))

   def initUI(self):
      self.setWindowModality(Qt.ApplicationModal)
      self.setWindowTitle("Create Chat")

      self.grid = QGridLayout(self)

      self.chat_name_label = QLabel("Chat Name:")
      self.grid.addWidget(self.chat_name_label, 0, 0, 1, 1)
      self.chat_name_field = QLineEdit()
      self.grid.addWidget(self.chat_name_field, 0, 1, 1, 3)

      self.unadded_friends = QListWidget()
      self.unadded_friends.setSortingEnabled(True)
      self.grid.addWidget(self.unadded_friends, 1, 0, 4, 2)

      self.added_friends = QListWidget()
      self.added_friends.setSortingEnabled(True)
      self.grid.addWidget(self.added_friends, 1, 3, 4, 1)

      self.add_friend_button = QPushButton(">>")
      self.add_friend_button.pressed.connect(self.addFriend)
      self.grid.addWidget(self.add_friend_button, 2, 2, 1, 1)

      self.remove_friend_button = QPushButton("<<")
      self.remove_friend_button.pressed.connect(self.removeFriend)
      self.grid.addWidget(self.remove_friend_button, 3, 2, 1, 1)

      self.create_button = QPushButton("Create")
      self.create_button.pressed.connect(self.createChat)
      self.grid.addWidget(self.create_button, 5, 0, 1, 4)

      self.cancel_button = QPushButton("Cancel")
      self.cancel_button.pressed.connect(self.cancel)
      self.grid.addWidget(self.cancel_button, 6, 0, 1, 4)

   def addFriend(self):
      selected_friends = self.unadded_friends.selectedItems()
      for friend in selected_friends:
         self.unadded_friends.takeItem(self.unadded_friends.row(friend))
         self.added_friends.addItem(friend)

   def removeFriend(self):
      selected_friends = self.added_friends.selectedItems()
      for friend in selected_friends:
         self.added_friends.takeItem(self.added_friends.row(friend))
         self.unadded_friends.addItem(friend)

   def createChat(self):
      self.created_chat = True
      self.chat_name = self.chat_name_field.text()
      for i in range(self.added_friends.count()):
         self.participants.append(self.added_friends.item(i).text())
      config.chats[self.chat_name] = {"participants": self.participants}
      self.close()

   def cancel(self):
      self.close()

class AddFriendDialog(QDialog):
   def __init__(self, client_socket):
      super().__init__()
      self.client_socket = client_socket 
      self.client_socket.recv_user_search.connect(self.recvUserSearch)
      self.selected_user = None
      self.initUI()

   def initUI(self):
      self.grid = QGridLayout(self)

      self.search_box_label = QLabel("Search:")
      self.grid.addWidget(self.search_box_label, 0, 0, 1, 1)

      self.search_box = QLineEdit()
      self.grid.addWidget(self.search_box, 0, 1, 1, 2)

      self.search_button = QPushButton("Search")
      self.search_button.pressed.connect(self.searchUser)
      self.grid.addWidget(self.search_button, 0, 3, 1, 1)

      self.search_result = QListWidget()
      self.grid.addWidget(self.search_result, 1, 0, 2, 2)

      #TODO get user avatars to work
      self.add_friend_button = QPushButton("Add Friend")
      self.add_friend_button.pressed.connect(self.addFriend)
      self.grid.addWidget(self.add_friend_button, 1, 2, 1, 2)

      self.cancel_button = QPushButton("Cancel")
      self.cancel_button.pressed.connect(self.cancel)
      self.grid.addWidget(self.cancel_button, 2, 2, 1, 2)

   def searchUser(self):
      self.client_socket.searchUser(self.search_box.text())

   def recvUserSearch(self, found_users):
      self.search_result.clear()
      for user in found_users:
         self.search_result.addItem(QListWidgetItem(user))

   def addFriend(self):
      self.selected_user = self.search_result.selectedItems()[0].text()
      config.friends[self.selected_user] = {}
      self.close()

   def cancel(self):
      self.close()
