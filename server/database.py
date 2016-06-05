#TODO
#storing the users in json is a bad idea (Imagine the ram requirements in prod)
#this will be replaced with sql or mongo eventually, but json works for testing :)

import json, hashlib, binascii, os

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

def create_user(request):
   #TODO return a response for the server to send (or put the checks in server.py)
   salt = binascii.hexlify(os.urandom(32)).decode("utf-8")
   password_hash = hash_password(request["password"], salt)
   user = {"password": {"hash":password_hash, "salt":salt}, "email":request["email"]}
   users[request["username"]] = user
   return True

def authenticate(username, password):
   global users
   if not username in users:
      return False
   user = users[username]
   password_hash = hash_password(password, user["password"]["salt"])
   return password_hash == user["password"]["hash"]

def hash_password(password, salt):
   password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 1000000)
   password_hash = binascii.hexlify(password_hash).decode("utf-8")
   return password_hash

def searchUsers(query):
   found_users = []
   for user in users:
      if user.startswith(query):
         found_users.append(user)
   return found_users
