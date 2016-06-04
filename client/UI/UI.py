import config
import network
import sys
from PyQt5.QtWidgets import QApplication
from UI.LoginWindow import LoginWindow
from UI.MainWindow import MainWindow

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

