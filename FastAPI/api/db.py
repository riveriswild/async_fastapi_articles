import os
from dotenv import load_dotenv
from databases import Database
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

Article = Table(
    "article",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(100)),
    Column("description", String(500)),
)

database = Database(SQLALCHEMY_DATABASE_URL)