# madeinkz

**Project Description:**

The project aims to research the origin of goods and develop a database to record product and producer certifications. The goal is to create a system that will collect, structure, and analyze information about certificates of origin, producers, products, and other related data.

---

## Project Structure

### Scripts

1. `database/create_db.py`Creates the PostgreSQL database.
2. `parse_to_csv/parse_atameken.py`Downloads data from Google Sheets and saves it as CSV files in the `results` folder.
3. `parse_to_db/1_1-8.py`Reads CSV files from the `results` folder and inserts the data into the previously created database. The `main.py` script runs scripts from 1 to 8.
4. `parse_to_opengov/parse_to_opengov.py`
   Uploads CSV files from the `datasets` folder to `data.opengov.kz` via API.

---

### Folders and Files

1. `datasets/`Folder containing the CSV files to be uploaded to `data.opengov.kz`.
2. `results/`Folder where CSV files are saved after running the `parse_atameken.py` script.
3. `sql/`SQL scripts for working with the database:

   - `create_tables.sql` — Code to create tables in the PostgreSQL database.

---

## How to Run the Project

**.ENV file:**

Change .env.example to .env file and change parameters of your database and SCAN api.

**Parameters for database**

| Variable Name | Description                         | Value      |
| ------------- | ----------------------------------- | ---------- |
| DB_NAME       | Name of the database                | made_in_kz |
| DB_USER       | Username to connect to the database | example    |
| DB_PASSWORD   | Password for the database user      | example    |
| DB_HOST       | Address of the database server      | localhost  |
| DB_PORT       | Port on which the database listens  | 5432       |


**Parameters for SCAN API**

| Variable Name   | Description                                  | Value                   |
| --------------- | -------------------------------------------- | ----------------------- |
| CKAN_URL        | Base URL of the CKAN data portal             | https://data.opengov.kz |
| API_KEY         | API key for authenticating with the CKAN API | example                 |
| ORGANIZATION_ID | ID of your organization on the CKAN portal   | example                 |

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

Run the `parse_to_opengov.py` script to upload the CSV files from the `datasets` folder to `data.opengov.kz` via the API. Parameters like CKAN_URL, API_KEY, ORGANIZATION_I can be changed in .env.example file.

2 options to run script. 

Change parameters in .env.example file and run.

```
python parse_to_db/main.py
```

Run the script with CKAN parameters specified via command-line flags:

| Variable                | Description                                                      |
| ----------------------- | ---------------------------------------------------------------- |
| https://data.opengov.kz | The URL of the CKAN                                              |
| YOUR_API_KEY            | Your personal API key used to authenticate and authorize access |
| your-org-id             | The organization ID                                            |

```
python parse_to_opengov.py --ckan-url "https://data.opengov.kz" --api-key "YOUR_API_KEY" --org-id "your-org-id"
```

### Important Notes

* Change .env.example to .env
* All scripts use an API key for access to the `data.opengov.kz` system. Ensure you have the correct API key.
* You will need PostgreSQL installed and configured on your machine to work with the database.
* Make sure all required Python libraries are installed. You can install them using the following command:
  `pip install -r requirements.txt`

## Data Sources

All data for this project was collected from https://atameken.kz/ru/services/56-reestr-sertifikatov-o-proishozhdenii-tovara

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
