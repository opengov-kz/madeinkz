import os
import psycopg2
import csv
import logging
from dotenv import load_dotenv
from datetime import datetime

log_file = "project/scripts/parse_to_db/logs/import_log.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

load_dotenv()

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    print("✅ Подключение к базе данных успешно.")
    logging.info("✅ Подключение к базе данных успешно.")
except Exception as e:
    print(f"❌ Ошибка при подключении к базе данных: {e}")
    logging.error(f"❌ Ошибка при подключении к базе данных: {e}")
    exit(1)

csv_file = "project/results/goods_certificates_1_1.csv"

def parse_date(date_str):
    """Парсинг даты из строки."""
    if not date_str or date_str.strip() == "":
        return None
    date_str = date_str.strip()
    try:
        if len(date_str) == 4:
            return datetime.strptime(date_str, "%Y").date()
        elif len(date_str) == 10 and "." in date_str:
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        logging.warning(f"⚠️ Ошибка парсинга даты: {date_str}")
        return None

def parse_float(value):
    """Парсинг числа из строки с удалением нечисловых символов и лишних запятых."""
    if not value or value.strip() == "":
        return None
    try:
        cleaned_value = ''.join(c for c in value if c.isdigit() or c == ',')
        
        if cleaned_value.count(',') > 1:
            cleaned_value = cleaned_value.replace(',', '', cleaned_value.count(',') - 1)
        
        cleaned_value = cleaned_value.replace(",", ".")
        
        return float(cleaned_value)
    except ValueError:
        logging.warning(f"⚠️ Ошибка парсинга числа: {value}")
        return None

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    block_start = 1
    block_end = 1000
    current_block_start = block_start

    for row_number, row in enumerate(reader, start=1):
        if row_number == block_start:
            log_msg = f"🔍 Начало обработки строк {block_start}-{block_end}"
            print(log_msg)
            logging.info(log_msg)

        try:
            cur.execute("SELECT id FROM rpp WHERE code = %s OR name = %s", 
                        (row["Код РПП"], row["Наименование РПП"]))
            rpp = cur.fetchone()
            if rpp:
                rpp_id = rpp[0]
            else:
                cur.execute("INSERT INTO rpp (name, code) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET code = EXCLUDED.code RETURNING id",
                            (row["Наименование РПП"], row["Код РПП"]))
                rpp_id = cur.fetchone()[0]

            cur.execute("INSERT INTO manufacturers (bin_iin, name, legal_address) VALUES (%s, %s, %s) ON CONFLICT (bin_iin) DO NOTHING",
                        (row["ИИН/ БИН производителя"], row["Наименование производителя"], row["Адрес производителя"]))

            quantity_value = parse_float(row["Количество товара"])
            cur.execute("SELECT id FROM products WHERE tn_ved_eaes = %s AND md5(name) = md5(%s)",
                        (row["Код ТН ВЭД"], row["Наименование товара"]))
            product = cur.fetchone()
            if product:
                product_id = product[0]
            else:
                cur.execute("INSERT INTO products (tn_ved_eaes, name, kp_ved, quantity, unit_measurement, unit_code, dvc) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING id",
                            (row["Код ТН ВЭД"], row["Наименование товара"], row["Код КП ВЭД"], quantity_value, row["Единица измерения"], row["Код единицы измерения"], parse_float(row["ДВЦ"])) )
                product = cur.fetchone()
                product_id = product[0] if product else None

            cur.execute("SELECT id FROM category_certificates WHERE name = %s", (row["Категория"],))
            category = cur.fetchone()
            if not category:
                cur.execute("INSERT INTO category_certificates (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id",
                            (row["Категория"],))
                category_id = cur.fetchone()[0]
            else:
                category_id = category[0]

            issue_date = parse_date(row["Дата выдачи"])
            date_ending = parse_date(row["Дата окончания действия сертификата"])

            cur.execute("SELECT id FROM certificates WHERE certificate_number = %s",
                        (row["Номер сертификата происхождения"],))
            certificate = cur.fetchone()
            if not certificate:
                cur.execute("INSERT INTO certificates (rpp_id, manufacturer_bin_iin, product_id, category_id, certificate_number, blank_number, issue_date, purpose_receipt, status, date_ending) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                            (rpp_id, row["ИИН/ БИН производителя"], product_id, category_id, row["Номер сертификата происхождения"], row["Номер бланка"], issue_date, row["Цель получения сертификата"], row["Статус сертификата"], date_ending))
                certificate_id = cur.fetchone()[0]
            else:
                certificate_id = certificate[0]

            success_msg = f"✅ Строка {row_number} обработана успешно."

        except Exception as e:
            error_msg = f"❌ Ошибка при обработке строки {row_number}: {e}"
            print(error_msg)
            logging.error(error_msg)

        if row_number == block_end:
            log_msg = f"🔍 Завершена обработка строк {block_start}-{block_end}"
            print(log_msg)
            logging.info(log_msg)

            block_start += 1000
            block_end += 1000

conn.commit()
cur.close()
conn.close()

print("🏁 Обработка завершена!")
logging.info("🏁 Обработка завершена!")
