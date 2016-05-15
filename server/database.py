#TODO
#storing the users in json is a bad idea (Imagine the ram requirements in prod)
#this will be replaced with sql or mongo eventually, but json works for testing :)

import json, hashlib, binascii

users = {}

def init():
   global users
   users_file = open("users.json")
   users = json.loads(users_file.read())
   users_file.close()

def save():
   global users
   users_file = open("users.json", "w")
   users_file.write(json.dumps(users))
   users_file.close()

def authenticate(username, password):
   global users
   user = users[username]
   if not user:
      return False
   password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), user["password"]["salt"].encode("utf-8"), 1000000)
   password_hash = binascii.hexlify(password_hash).decode("utf-8")
   return password_hash == user["password"]["hash"]
