import pandas as pd
import requests
import io
import re
import chardet
import os

def parse_public_google_sheet(spreadsheet_id, sheet_id=0):
    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            encoding_result = chardet.detect(response.content)
            detected_encoding = encoding_result['encoding']
            
            try:
                df = pd.read_csv(io.StringIO(response.content.decode(detected_encoding)), low_memory=False)
            except UnicodeDecodeError:
                df = pd.read_csv(io.StringIO(response.content.decode('utf-8', errors='replace')), low_memory=False)
            
            print(f"Успешно получены данные из таблицы. Всего строк: {len(df)}")
            return df
        else:
            print(f"Ошибка при получении данных. Код статуса: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"Произошла ошибка при парсинге таблицы: {str(e)}")
        return None

def clean_data(df):
    df = df.dropna(how='all')
    df = df.drop_duplicates()
    df.columns = [col.strip() for col in df.columns]
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    def clean_text(x):
        if isinstance(x, str):
            x = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', x)
            return x
        return x
    
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(clean_text)
    
    return df

def save_data(df, output_file):
    if df is not None:
        try:
            output_dir = "results"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, output_file)
            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"Данные сохранены в файл: {output_path}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {str(e)}")

def main():
    spreadsheets = [
        {"id": "168yLL5EJwDQCFKKR1CkcplcEiAxuczdEom8uX0kXBUg", "sheets": [734652276]},
    ]
    
    print("Парсинг нескольких таблиц Google Sheets")
    
    for i, spreadsheet in enumerate(spreadsheets, start=1):
        spreadsheet_id = spreadsheet["id"]
        
        for j, sheet_id in enumerate(spreadsheet["sheets"], start=1):
            print(f"\nОбрабатываем таблицу {i}, лист {j} (ID: {spreadsheet_id}, Sheet ID: {sheet_id})")
            
            df = parse_public_google_sheet(spreadsheet_id, sheet_id)
            
            if df is not None:
                df = clean_data(df)
                save_data(df, f'goods_certificates_{i}_{j}.csv')
    
    print("\nВсе данные успешно обработаны и сохранены.")

if __name__ == "__main__":
    main()