import psycopg2
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


    cursor = connection.cursor()
    with open(csv_file_path, 'r', encoding="utf-8") as file:
        next(file)
        cursor.copy_from(file, table_name, sep=',')

except Exception as _ex:
    print('Exception occurred:', _ex)

