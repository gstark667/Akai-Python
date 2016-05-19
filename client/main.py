import config
import ui

config.init()
user_interface = ui.UI()
user_interface.exec()
print("Exit")
user_interface.main_window.client_socket.disconnect()
config.save()
