from Crypto.PublicKey import RSA
import hashlib

#password is entered by the user (or stored in file)
#TODO hash the password before it gets sent to the server
#     (prevents rouge server from getting user passwords)
password = b"potato"
#salt will be stored on server and passed to client for use in key generation
#(prevents password confirmation through brute force public key generation)
salt     = b"salty"

class PRNG(object):

   def __init__(self, password, salt):
      self.password = password
      self.salt     = salt
      self.cur_hash = self.salt + self.password
      for i in range(1000000):
         self.cur_hash = hashlib.sha256(self.salt + self.cur_hash).digest()
      self.buffer   = b""

   def __call__(self, n):
      while len(self.buffer) < n:
          self.cur_hash = hashlib.sha256(self.salt + self.cur_hash).digest()
          self.buffer += self.cur_hash
      result, self.buffer = self.buffer[:n], self.buffer[n:]
      return result

def generate_key(password, salt, length):
   return RSA.generate(length, randfunc=PRNG(password, salt))

key = generate_key(password, salt, 2048)
print(key.exportKey())
print(key.publickey().exportKey())

privKey = key
pubKey  = key.publickey()

text = b"Hello World"
etext = pubKey.encrypt(text, 'x')
dtext = privKey.decrypt(etext)

print(text)
print(etext)
print(dtext)
