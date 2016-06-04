import config
from UI.UI import UI

config.init()
user_interface = UI()
user_interface.exec()
print("Exit")
user_interface.main_window.client_socket.disconnect()
config.save()
