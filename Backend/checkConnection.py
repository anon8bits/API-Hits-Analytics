import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('POSTGRES_URI')

try:
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Connected to PostgreSQL database. Version: {db_version}")
    cursor.close()
    connection.close()
except Exception as error:
    print(f"Error connecting to PostgreSQL database: {error}")
