from pymongo import MongoClient
from sqlalchemy.orm import declarative_base
import os

Base = declarative_base()

def get_db():
   try:
      CONNECTION_STRING = os.getenv("DATABASE_URL")
      client = MongoClient(CONNECTION_STRING)
 
      print("Successfully connected")

      return client['lanchonete_pagamento_database']
   
   except Exception as e:
      print("Connection failed:", e)
 
if __name__ == "__main__":
   dbname = get_db()