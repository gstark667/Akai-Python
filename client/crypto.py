from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto import Random
import hashlib
import binascii
import struct

#password is entered by the user (or stored in file)
#TODO hash the password before it gets sent to the server
#     (prevents rouge server from getting user passwords)
#password = b"potato"
#salt will be stored on server and passed to client for use in key generation
#(prevents password confirmation through brute force public key generation)
#salt     = b"salty"

class PRNG(object):

   def __init__(self, password, salt):
      self.password = password
      self.salt     = salt
      self.cur_hash = self.salt + self.password
      for i in range(100000):
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

class MessagePacker():
   def __init__(self, send_key, recv_key, block_size=16):
      self.send_key = send_key
      self.recv_key = recv_key
      self.block_size = block_size

   #TODO enforce encoding
   def packageMessage(self, message):
      signature = self.send_key.sign(message, 'a')[0]
      signature_bytes = signature.to_bytes(int(signature.bit_length()/8), 'big')
      padding_block = self.padMessage(b"")
      padded_signature = self.padMessage(signature_bytes)
      padded_message = self.padMessage(message)
      length = len(padding_block + padded_signature + padded_message) + 2*self.block_size
      padded_length = self.padMessage(length.to_bytes(16, 'big'))
      packaged_message = padding_block + padded_length + padded_signature + padded_message

      encrypted_message = []
      while len(packaged_message) > 0:
         encrypted_message.append(packaged_message[0:256])
         packaged_message = packaged_message[256:]
      return encrypted_message

   def padMessage(self, message):
      to_pad = self.block_size - (len(message)%self.block_size)
      pad = b""
      for _ in range(to_pad):
         pad += bytes([to_pad])
      return message + pad

class MessageUnpacker():
   def __init__(self, recv_key):
      self.recv_key = recv_key
      self.unpacked_message = ""
      self.block_size = 0

   def unpackMessage(self, message):
      dencrypted_message = recv_key.decrypt(message)
      print(decrypted_message)

#send key is private
#recv key is public
key1 = generate_key(b"test", b"salt", 2048)
key2 = generate_key(b"test2", b"salt", 2048)



packer = MessagePacker(key1, key2.publickey(), 16)
packed_message = packer.packageMessage(b"Hello Alice")

#message = b"Hello Alice"
#signature = key1.sign(message, 'a')

#emessage = key2.publickey().encrypt(message, 'a')


#print(key2.decrypt(emessage))
#print(key1.publickey().verify(message, signature))
print(key1.exportKey())
print(key1.publickey().exportKey())

#privKey = key
#pubKey  = key.publickey()

#text = b"Hello World"
#etext = pubKey.encrypt(text, 'x')
#dtext = privKey.decrypt(etext)

#print(text)
#print(etext)
#print(dtext)
