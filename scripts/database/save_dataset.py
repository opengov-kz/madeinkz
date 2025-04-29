import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)
SQL_FILE = "sql/to_save_fromDB_to_csv.sql" 

try:
    if not os.path.exists(SQL_FILE):
        raise FileNotFoundError(f"Файл {SQL_FILE} не найден.")

    env = os.environ.copy()
    env["PGPASSWORD"] = DB_PASSWORD

    result = subprocess.run([
        "psql",
        "-h", DB_HOST,
        "-p", str(DB_PORT),
        "-U", DB_USER,
        "-d", DB_NAME,
        "-f", SQL_FILE
    ], env=env, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"SQL-скрипт {SQL_FILE} успешно выполнен.")
    else:
        print(f"Ошибка при выполнении SQL-скрипта:\n{result.stderr}")

except Exception as e:
    print(f"Ошибка: {e}")
