import os
import psycopg2
import csv
import logging
from dotenv import load_dotenv
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scripts/parse_to_db/logs/import_log4.log"),
        logging.StreamHandler()
    ]
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
    logging.info("✅ Подключение к базе данных успешно.")
except Exception as e:
    logging.error(f"Ошибка подключения к базе данных: {e}")
    exit(1)

csv_file = "results/goods_certificates_4_1.csv"

def parse_date(date_str):
    if not date_str or date_str.strip() == "":
        return None
    date_str = date_str.strip()
    try:
        if len(date_str) == 4:
            return datetime.strptime(date_str, "%Y").date()
        elif "." in date_str:
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        elif "-" in date_str:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        logging.warning(f"Ошибка преобразования даты: {date_str}")
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
            cur.execute(
                "INSERT INTO rpp (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id",
                (row["Наименование РПП"],)
            )
            rpp = cur.fetchone()
            if not rpp:
                cur.execute("SELECT id FROM rpp WHERE name = %s", (row["Наименование РПП"],))
                rpp = cur.fetchone()
            rpp_id = rpp[0] if rpp else None

            cur.execute(
                """INSERT INTO manufacturers (bin_iin, name, legal_address)
                   VALUES (%s, %s, %s) ON CONFLICT (bin_iin) DO NOTHING""",
                (row["ИИН/БИН отправителя/экспортера"], row["Наименование отправителя/экспортера"], row["Адрес отправителя/экспортера"])
            )
            
            cur.execute(
                "INSERT INTO certificate_forms (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id",
                (row["Форма сертификата"],)
            )
            form = cur.fetchone()
            if not form:
                cur.execute("SELECT id FROM certificate_forms WHERE name = %s", (row["Форма сертификата"],))
                form = cur.fetchone()
            form_id = form[0] if form else None

            cur.execute(
                "INSERT INTO countries (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id",
                (row["Страна происхождения товара"],)
            )
            origin_country = cur.fetchone()
            if not origin_country:
                cur.execute("SELECT id FROM countries WHERE name = %s", (row["Страна происхождения товара"],))
                origin_country = cur.fetchone()
            export_country_id = origin_country[0] if origin_country else None

            import_country_key = "Страна получателя/импортера" if "Страна получателя/импортера" in row else "Страна получателя/ импортера"
            
            cur.execute(
                "INSERT INTO countries (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id",
                (row[import_country_key],)
            )
            import_country = cur.fetchone()
            if not import_country:
                cur.execute("SELECT id FROM countries WHERE name = %s", (row[import_country_key],))
                import_country = cur.fetchone()
            import_country_id = import_country[0] if import_country else None

            cur.execute(
                "SELECT id FROM products WHERE tn_ved_eaes = %s AND name = %s",
                (row["Код ТН ВЭД"], row["Наименование товара"])
            )
            product = cur.fetchone()
            if not product:
                cur.execute(
                    """INSERT INTO products (tn_ved_eaes, name)
                       VALUES (%s, %s) RETURNING id""",
                    (row["Код ТН ВЭД"], row["Наименование товара"])
                )
                product = cur.fetchone()
            product_id = product[0] if product else None


            cur.execute(
                "SELECT id FROM certificates WHERE certificate_number = %s",
                (row["Номер сертификата происхождения"],)
            )
            certificate = cur.fetchone()
            if not certificate:
                cur.execute(
                    """INSERT INTO certificates (rpp_id, manufacturer_bin_iin, product_id, 
                       certificate_number, blank_number, issue_date, origin_criterion, 
                       status, export_country_id, import_country_id, form_id) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                    (rpp_id, row["ИИН/БИН отправителя/экспортера"], product_id, 
                     row["Номер сертификата происхождения"], row["Номер бланка"], 
                     parse_date(row["Дата выдачи"]), row["Критерий происхождения"], 
                     row["Статус сертификата"], export_country_id, import_country_id, form_id)
                )
                certificate = cur.fetchone()
            certificate_id = certificate[0] if certificate else None
        
        except Exception as e:
            logging.error(f"Ошибка при обработке строки {row_number}: {e}")

        if row_number == block_end:
            log_msg = f"🔍 Завершена обработка строк {block_start}-{block_end}"
            print(log_msg)
            logging.info(log_msg)

            block_start += 1000
            block_end += 1000

conn.commit()
cur.close()
conn.close()

logging.info("Импорт завершен!")
