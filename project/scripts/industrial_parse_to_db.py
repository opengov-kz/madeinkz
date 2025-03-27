import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv  

load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

csv_file = "project/results/goods_certificates_1_1.csv"
df = pd.read_csv(csv_file, encoding="utf-8", dtype=str, sep=None, engine="python") 

def clean_date(date_str):
    if date_str in ["-", "не установлен", None] or pd.isna(date_str):
        return None
    try:
        return pd.to_datetime(date_str, format="%Y.%m.%d").date()  
    except ValueError:
        return None  

for index, row in df.iterrows():
    date_included = clean_date(row["Дата включения в Реестр"])
    date_of_change = clean_date(row["Дата внесения изменений и/или дополнений"])
    issue_date = clean_date(row["Дата выдачи документа об оценке соотвествия"])
    end_date = clean_date(row["Дата окончания документа об оценке соотвествия"])
    
    manufacturer_data = {
        "bin_iin": row["БИН/ИИН"],
        "name": row["Наименование производителей товаров, работ, услуг"],
        "legal_address": row["Юридический адрес"],
        "actual_address": row["Почтовый (фактический) адрес"],
        "phone": row["Телефон"],
        "email": row["Электронный адрес"],
        "website": row["Web - сайт"],
        "date_included_in_the_registry": date_included,
        "date_of_change": date_of_change,
        "number_of_employees": int(row["Количество сотрудников"]) if row["Количество сотрудников"].isdigit() else None,
        "oced_code": row["Вид деятельности согласно ОКЭД (перв, вторич.)"],
        "kato": row["Регион согласно КАТО"],
        "production_capacity": row["Производственная мощность, кол-во единиц в год"]
    }
    df_manufacturer = pd.DataFrame([manufacturer_data])
    try:
        df_manufacturer.to_sql("manufacturers", engine, if_exists="append", index=False)
    except IntegrityError:
        print(f"Запись с bin_iin {row['БИН/ИИН']} уже существует. Пропускаем.")
    
    product_data = {
        "tn_ved_eaes": row["ТН ВЭД ЕАЭС"],
        "name": row["Наименование товаров (категория), работ, услуг"],
        "kp_ved": row["КП ВЭД"],
        "unit_measurement": row.get("Единица измерения", None),  
        "unit_code": row.get("Код единицы измерения", None),  
        "quantity": int(row["Количество сотрудников"]) if row["Количество сотрудников"].isdigit() else None
    }
    df_product = pd.DataFrame([product_data])
    try:
        df_product.to_sql("products", engine, if_exists="append", index=False)
    except IntegrityError:
        print(f"Запись с tn_ved_eaes {row['ТН ВЭД ЕАЭС']} уже существует. Пропускаем.")
    
    document_data = {
        "document_id": row["Номер документа об оценке соотвествия"],
        "issue_date": issue_date,
        "end_date": end_date,
        "authorisation_licence": row["Номер и дата лицензии или разрешения"],
        "manufacturer_bin_iin": row["БИН/ИИН"]
    }
    df_document = pd.DataFrame([document_data])
    try:
        df_document.to_sql("document_compliances", engine, if_exists="append", index=False)
    except IntegrityError:
        print(f"Запись с document_id {row['Номер документа об оценке соотвествия']} уже существует. Пропускаем.")

print("Данные успешно загружены в базу данных!")
