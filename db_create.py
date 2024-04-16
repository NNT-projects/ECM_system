import psycopg2
import csv

try:
    connection = psycopg2.connect(
        dbname='testDB',
        user='postgres',
        host='localhost',
        password='1234',
        port='5432'
    )
    csv_file_path = 'C:/Users/pengv/Downloads/X_train.csv'

    connection.autocommit = True

    table_name = 'data_engine'

    cur = connection.cursor()
    with open(csv_file_path, 'r', encoding="utf-8") as f:
        next(f)
        cur.copy_from(f, table_name, sep=',')

    '''
    columns = '"reportts" TIMESTAMP, "acnum" VARCHAR(255), "pos" INTEGER, "fltdes" INTEGER, "dep" VARCHAR(255), "arr" VARCHAR(255)'
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        count = 0
        for header in headers:
            if count < 6:
                count += 1
                continue
            columns += f', "{header}" REAL'
    
    #with connection.cursor() as cursor:
    #    cursor.execute("SELECT VERSION();")
    #    print(f"Server version: {cursor.fetchone()}")


    with connection.cursor() as cursor:
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

    connection.close()
    print("Connection closed")
    '''

except Exception as _ex:
    print('Exception occurred:', _ex)

