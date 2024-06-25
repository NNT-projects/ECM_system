import psycopg2
import csv
from params_for_DB import *

try:
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        host=host,
        password=password,
        port=port
    )

    connection.autocommit = True

    cur = connection.cursor()

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        columns = ', '.join([f'"{header}" VARCHAR(255)' for header in headers])
        print(columns)

    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        next(f)  # Skip header
        cur.copy_from(f, table_name, sep=',', null='')

    cur.execute(f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS "egtm" VARCHAR(255)')

except Exception as _ex:
    print('Exception occurred:', _ex)