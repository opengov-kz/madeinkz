import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def read_sql_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def create_database():
    conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"База данных {DB_NAME} создана!")
    else:
        print(f"База данных {DB_NAME} уже существует.")

    cur.close()
    conn.close()

def create_tables():
    sql_script = read_sql_file("project/sql/create_tables.sql")
    
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    cur.execute(sql_script)
    conn.commit()
    
    print("Таблицы успешно созданы!")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_database()
    create_tables()
