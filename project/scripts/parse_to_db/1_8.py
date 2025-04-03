import os
import psycopg2
import csv
import logging
from dotenv import load_dotenv
from datetime import datetime
from psycopg2.extras import execute_batch

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("project/scripts/parse_to_db/logs/import_log8.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

load_dotenv()

logging.info("Подключение к базе данных...")
try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    logging.info("Успешное подключение к базе данных.")
except Exception as e:
    logging.error(f"Ошибка подключения к БД: {e}")
    exit(1)

csv_file = "project/results/goods_certificates_8_1.csv"

import logging
from datetime import datetime

def parse_date(date_str):
    if not date_str or date_str.strip() in ["", "-", "Срок не установлен", "не установлен", "бессрочно"]:
        return None
    
    date_str = date_str.strip()
    date_str = ''.join(c for c in date_str if c.isdigit() or c in ".-/")
    
    if "\n" in date_str:
        date_str = date_str.split("\n")[0].strip()
    
    try:
        if len(date_str) == 4 and date_str.isdigit():
            return datetime.strptime(date_str, "%Y").date()
        
        elif date_str.count(".") == 2:
            parts = date_str.split(".")
            if len(parts) == 3:
                if len(parts[0]) == 4 and parts[0].isdigit():
                    year, month, day = parts
                    month = month.zfill(2)
                    day = day.zfill(2)
                    return datetime.strptime(f"{year}.{month}.{day}", "%Y.%m.%d").date()
                elif len(parts[2]) == 4 and parts[2].isdigit():
                    day, month, year = parts
                    month = month.zfill(2)
                    day = day.zfill(2)
                    return datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y").date()

        elif date_str.count("-") == 2 and len(date_str) == 10:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        
        formats = ["%Y.%m.%d", "%d.%m.%Y", "%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        raise ValueError(f"Неподдерживаемый формат даты: {date_str}")
    
    except ValueError as e:
        logging.warning(f"Ошибка преобразования даты: '{date_str}' — {str(e)}")
        return None

block_start = 1
block_end = 1000
current_block_start = block_start

industrial_certificates_data = []
manufacturers_data = []
products_data = []
certificates_data = []
document_compliances_data = []

try:
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            if i == block_start:
                logging.info(f"🔍 Начало обработки строк {block_start}-{block_end}")
            
            try:
                certificate_number = row["Номер документа об оценке соотвествия"]
                bin_iin = row["БИН/ИИН"]
                manufacturer_name = row["Наименование производителей товаров, работ, услуг"]
                legal_address = row["Юридический адрес"]
                product_name = row["Наименование товаров (категория), работ, услуг"][:255]  # Ограничение на 255 символов
                tn_ved = row["ТН ВЭД ЕАЭС"]
                issue_date = parse_date(row["Дата выдачи документа об оценке соотвествия"])
                end_date = parse_date(row["Дата окончания документа об оценке соотвествия"])
                licence = row["Номер и дата лицензии или разрешения"]

                # Добавляем данные в списки для пакетной вставки
                industrial_certificates_data.append((certificate_number,))
                manufacturers_data.append((bin_iin, manufacturer_name, legal_address))
                products_data.append((product_name, tn_ved))
                certificates_data.append((certificate_number, product_name, bin_iin))
                document_compliances_data.append((certificate_number, issue_date, end_date, licence, bin_iin))

                if i == block_end:
                    logging.info(f"🔍 Завершена обработка строк {block_start}-{block_end}")
                    block_start += 1000
                    block_end += 1000

            except Exception as e:
                if isinstance(e, ValueError) and "Неподдерживаемый формат даты" in str(e):
                    logging.error(f"Ошибка преобразования даты в строке {i}: {e}")
                else:
                    logging.error(f"Ошибка при обработке строки {i}: {e}")
            
            if i == block_end:
                execute_batch(
                    cur,
                    "INSERT INTO industrial_certificates (certificate_number) VALUES (%s) ON CONFLICT (certificate_number) DO NOTHING",
                    industrial_certificates_data
                )
                execute_batch(
                    cur,
                    "INSERT INTO manufacturers (bin_iin, name, legal_address) VALUES (%s, %s, %s) ON CONFLICT (bin_iin) DO NOTHING",
                    manufacturers_data
                )
                execute_batch(
                    cur,
                    "INSERT INTO products (name, tn_ved_eaes) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING",
                    products_data
                )
                execute_batch(
                    cur,
                    "INSERT INTO certificates (industrial_certificate_id, product_id, manufacturer_bin_iin) VALUES "
                    "(%s, %s, %s) ON CONFLICT DO NOTHING",
                    certificates_data
                )
                execute_batch(
                    cur,
                    "INSERT INTO document_compliances (document_id, issue_date, end_date, authorisation_licence, manufacturer_bin_iin) "
                    "VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    document_compliances_data
                )

                industrial_certificates_data.clear()
                manufacturers_data.clear()
                products_data.clear()
                certificates_data.clear()
                document_compliances_data.clear()

                conn.commit()

except Exception as e:
    logging.error(f"Ошибка во время выполнения: {e}")
    conn.rollback()

finally:
    cur.close()
    conn.close()
    logging.info("Импорт завершен!")
