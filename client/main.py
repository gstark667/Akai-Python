import config
from UI.UI import UI

config.init()
user_interface = UI()
user_interface.exec()
print("Exit")
user_interface.disconnect()
config.save()
