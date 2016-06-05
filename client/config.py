import os
import json

#TODO different config dirs for different platforms
CONFIG_DIR = ""
ICON_DIR = ""
CHATS_CONFIG = "chats.conf"
FRIEND_CONFIG = "friend.conf"
USER_CONFIG = "user.conf"

chats = {}
friends = {}
user = {"username": ""}

def init():
   global CONFIG_DIR, ICON_DIR, CHATS_CONFIG, FRIEND_CONFIG, USER_CONFIG
   CONFIG_DIR = os.environ["HOME"] + "/.config/akai/"
   ICON_DIR = CONFIG_DIR + "icons/"
   CHATS_CONFIG = CONFIG_DIR + "chats.conf"
   FRIEND_CONFIG = CONFIG_DIR + "friend.conf"
   USER_CONFIG = CONFIG_DIR + "user.conf"

   if not os.path.exists(CONFIG_DIR):
      os.makedirs(CONFIG_DIR)

   loadChats()
   loadFriends()
   loadUser()

def save():
   saveChats()
   saveFriends()
   saveUser()

def loadChats():
   global chats 
   try:
      chats_file = open(CHATS_CONFIG, "r")
      chats = json.loads(chats_file.read())
   except:
      saveChats()
      print("unable to open chats config file")

def saveChats():
   global friends
   chats_file = open(CHATS_CONFIG, "w")
   chats_file.write(json.dumps(chats))

def loadFriends():
   global friends
   try:
      friends_file = open(FRIEND_CONFIG, "r")
      friends = json.loads(friends_file.read())
   except:
      saveFriends()
      print("unable to open friend config file")

def saveFriends():
   global friends
   friends_file = open(FRIEND_CONFIG, "w")
   friends_file.write(json.dumps(friends))

#TODO find a good way to store passwords locally
def loadUser():
   global user
   try:
      user_file = open(USER_CONFIG, "r")
      user = json.loads(user_file.read())
   except:
      saveUser()
      print("unable to open user config file")

def saveUser():
   global user
   user_file = open(USER_CONFIG, "w")
   user_file.write(json.dumps(user))
