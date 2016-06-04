import network
import config
from UI.Dialog import CreateAccountDialog
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal

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
