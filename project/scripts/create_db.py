import os
import psycopg2

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def create_database():
    """Создает базу данных, если она не существует"""
    conn = psycopg2.connect(
        dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
    cursor.close()
    conn.close()

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS Сертификаты (
        Код_РПП VARCHAR(255),
        Наименование_РПП VARCHAR(255),
        Номер_сертификата VARCHAR(255),
        Номер_бланка VARCHAR(255),
        Год_выдачи INT,
        Цель_получения_сертификата VARCHAR(255),
        Категория VARCHAR(255),
        ИИН_БИН_производителя VARCHAR(255),
        ИИН_БИН_получателя VARCHAR(255),
        Дата_окончания_действия DATE,
        Статус_сертификата VARCHAR(255),
        Дата_выдачи DATE
    );

    CREATE TABLE IF NOT EXISTS Сертификаты_на_продукцию (
        Номер_сертификата VARCHAR(255),
        Наименование_РПП VARCHAR(255),
        Форма_сертификата VARCHAR(255),
        Номер_бланка VARCHAR(255),
        ИИН_БИН_отправителя VARCHAR(255),
        Наименование_отправителя VARCHAR(255),
        Адрес_отправителя VARCHAR(255),
        Код_ТН_ВЭД VARCHAR(255),
        Критерий_происхождения VARCHAR(255),
        Страна_происхождения VARCHAR(255),
        Страна_получателя VARCHAR(255),
        Статус_сертификата VARCHAR(255),
        Дата_выдачи DATE
    );

    CREATE TABLE IF NOT EXISTS Индустриальные_сертификаты (
        Регистрационный_номер_индустриального_сертификата VARCHAR(255),
        БИН_ИИН VARCHAR(255),
        Наименование_производителей VARCHAR(255),
        Вид_деятельности_ОКЭД VARCHAR(255),
        Регион_КАТО VARCHAR(255),
        Юридический_адрес VARCHAR(255),
        Почтовый_адрес VARCHAR(255),
        Телефон VARCHAR(255),
        Электронный_адрес VARCHAR(255),
        Web_сайт VARCHAR(255),
        Производственная_мощность INT,
        ТН_ВЭД_ЕАЭС VARCHAR(255),
        КП_ВЭД VARCHAR(255),
        Номер_документа_о_оценке_соответствия VARCHAR(255),
        Дата_выдачи_документа DATE,
        Дата_окончания_документа DATE,
        Номер_и_дата_лицензии VARCHAR(255),
        Количество_сотрудников INT,
        Дата_включения_в_реестр DATE,
        Дата_внесения_изменений DATE,
        Дата_актуализации DATE
    );

    CREATE TABLE IF NOT EXISTS Производители (
        ИИН_БИН VARCHAR(255) PRIMARY KEY,
        Наименование_производителя VARCHAR(255),
        Адрес_производителя VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS Получатели (
        ИИН_БИН VARCHAR(255) PRIMARY KEY,
        Наименование_получателя VARCHAR(255),
        Адрес_получателя VARCHAR(255)
    );
    """
    cursor.execute(create_tables_sql)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database()
    create_tables()