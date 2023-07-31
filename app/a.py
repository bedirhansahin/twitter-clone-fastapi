from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os


load_dotenv()

DB_URL = str(os.environ.get("DB_URL"))

print(DB_URL)
print("postgresql://postgres:mypassword@db:5432/postgres")
