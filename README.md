# madeinkz

**Project Description:**

The project aims to research the origin of goods and develop a database to record product and producer certifications. The goal is to create a system that will collect, structure, and analyze information about certificates of origin, producers, products, and other related data.

---

## Project Structure

### Scripts

1. `database/create_db.py`Creates the PostgreSQL database.
2. `database/save_dataset.py`Saves data from DB in csv format.
3. `parse_to_csv/parse_atameken.py`Downloads data from Google Sheets and saves it as CSV files in the `results` folder.
4. `parse_to_db/1_1-8.py`Reads CSV files from the `results` folder and inserts the data into the previously created database. The `main.py` script runs scripts from 1 to 8.
5. `parse_to_opengov/parse_to_opengov.py`
   Uploads CSV files from the `datasets` folder to `data.opengov.kz` via API.

---

### Folders and Files

1. `datasets/`Folder containing the CSV files to be uploaded to `data.opengov.kz`.
2. `results/`Folder where CSV files are saved after running the `parse_atameken.py` script.
3. `sql/`SQL scripts for working with the database:

   - `create_tables.sql` — Code to create tables in the PostgreSQL database.
   - `to_save_fromDB_to_csv.sql` — SQL queries to save data from the database to CSV format for upload to `data.opengov.kz`.

---

## How to Run the Project

**Create the Database:**

Run the `create_db.py` script to create the database.

```bash
python database/create_db.py
```

**Download Data from Google Sheets:**

Run the `parse_atameken.py` script to download data from Google Sheets and save it as CSV files in the `results` folder.  

```
python parse_to_csv/parse_atameken.py
```

**Upload Data to the Database:**

Run the `main.py` script to read the CSV files saved in the `results` folder and insert them into the database.

```
python parse_to_db/main.py
```

**Upload Data to data.opengov.kz:**

Run the `parse_to_opengov.py` script to upload the CSV files from the `datasets` folder to `data.opengov.kz` via the API.

```
python parse_to_db/main.py
```

### Important Notes

* All scripts use an API key for access to the `data.opengov.kz` system. Ensure you have the correct API key.
* You will need PostgreSQL installed and configured on your machine to work with the database.
* Make sure all required Python libraries are installed. You can install them using the following command:
  `pip install -r requirements.txt`

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
