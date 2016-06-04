import config
import network
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton

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
