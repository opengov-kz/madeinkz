import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
SQL_FILE = "project\sql\create_tables.sql"  

try:
    conn = psycopg2.connect(
        dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    cursor.execute(f"CREATE DATABASE {DB_NAME};")
    print(f"База данных {DB_NAME} успешно создана!")
    
    cursor.close()
    conn.close()
    
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()
    
    with open(SQL_FILE, "r") as sql_file:
        sql_script = sql_file.read()
        cursor.execute(sql_script)
    
    conn.commit()
    print(f"SQL-скрипт {SQL_FILE} успешно выполнен!")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Ошибка: {e}")
