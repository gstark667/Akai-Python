import sqlite3

class Database:
   def __init__(self, database_file):
      self.conn = sqlite3.connect(database_file)

   def commit(self):
      self.conn.commit()

   def close(self):
      self.conn.close()

db = Database("users.db")
