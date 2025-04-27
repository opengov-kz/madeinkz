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
        logging.FileHandler("scripts/parse_to_db/logs/import_log8.log", encoding="utf-8"),
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
    logging.info("✅ Подключение к БД успешно.")
except Exception as e:
    logging.error(f"❌ Ошибка подключения: {e}")
    exit(1)

csv_file = "results/goods_certificates_8_1.csv"

block_size = 1000
batch = 1

manufacturers_data = []

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%d.%m.%Y").date() if date_str.strip() else None
    except ValueError:
        return None

def parse_int(int_str):
    try:
        return int(int_str.strip()) if int_str.strip() else None
    except ValueError:
        return None

try:
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            try:
                bin_iin = row["БИН/ИИН"].strip()
                manufacturer_name = row["Наименование производителей товаров, работ, услуг"].strip()
                legal_address = row["Юридический адрес"].strip()
                
                actual_address = row.get("Почтовый (фактический) адрес", "").strip() or None
                phone = row.get("Телефон", "").strip() or None
                email = row.get("Электронный адрес", "").strip() or None
                website = row.get("Web - сайт", "").strip() or None
                oced_code = row.get("Вид деятельности согласно ОКЭД (перв, вторич.)", "").strip() or None
                kato = row.get("Регион согласно КАТО", "").strip() or None
                production_capacity = row.get("Производственная мощность, кол-во единиц в год", "").strip() or None
                
                date_included = parse_date(row.get("Дата включения в Реестр", ""))
                date_of_change = parse_date(row.get("Дата внесения изменений и/или дополнений", ""))
                number_of_employees = parse_int(row.get("Количество сотрудников", ""))

                manufacturers_data.append((
                    bin_iin,
                    manufacturer_name,
                    legal_address,
                    actual_address,
                    phone,
                    email,
                    website,
                    date_included,
                    date_of_change,
                    number_of_employees,
                    oced_code,
                    kato,
                    production_capacity
                ))

            except Exception as e:
                logging.error(f"❗️Ошибка в строке {i}: {e}")
                continue

            if i % block_size == 0:
                logging.info(f"⬇️ Блок {batch}: строки {i - block_size + 1}-{i}")
                try:
                    execute_batch(
                        cur,
                        """INSERT INTO manufacturers (
                            bin_iin, name, legal_address, actual_address,
                            phone, email, website, date_included_in_the_registry,
                            date_of_change, number_of_employees, oced_code,
                            kato, production_capacity
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (bin_iin) DO NOTHING""",
                        manufacturers_data
                    )
                    conn.commit()
                    logging.info(f"✅ Блок {batch} успешно загружен.")
                except Exception as e:
                    conn.rollback()
                    logging.error(f"❌ Ошибка при загрузке блока {batch}: {e}")

                manufacturers_data.clear()
                batch += 1

    if manufacturers_data:
        logging.info(f"⬇️ Завершающий блок {batch}")
        try:
            execute_batch(
                cur,
                """INSERT INTO manufacturers (
                    bin_iin, name, legal_address, actual_address,
                    phone, email, website, date_included_in_the_registry,
                    date_of_change, number_of_employees, oced_code,
                    kato, production_capacity
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (bin_iin) DO NOTHING""",
                manufacturers_data
            )
            conn.commit()
            logging.info(f"✅ Завершающий блок {batch} успешно загружен.")
        except Exception as e:
            conn.rollback()
            logging.error(f"❌ Ошибка в завершающем блоке: {e}")

except Exception as e:
    logging.error(f"❌ Ошибка во время выполнения: {e}")
    conn.rollback()

finally:
    cur.close()
    conn.close()
    logging.info("📦 Импорт завершён.")