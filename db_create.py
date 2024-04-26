import psycopg2
import os
import csv

try:
    connection = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'testDB'),
        user=os.getenv('POSTGRES_USER', 'user'),
        host="localhost",
        password=os.getenv('POSTGRES_PASSWORD', '123'),
        port=os.getenv('POSTGRES_PORT', '5432')
    )

    # # Создание курсора для выполнения SQL-запросов
    # cursor = connection.cursor()

    # # Создание таблицы в базе данных
    # create_table_query = '''CREATE TABLE IF NOT EXISTS my_table (
    #                         id SERIAL PRIMARY KEY,
    #                         field1 VARCHAR(255),
    #                         field2 VARCHAR(255)
    #                     );'''
    # cursor.execute(create_table_query)
    # connection.commit()

    # # Вставка пары значений в таблицу
    # insert_query = """INSERT INTO my_table (field1, field2) VALUES (%s, %s);"""
    # record_to_insert = ('значение1', 'значение2')
    # cursor.execute(insert_query, record_to_insert)
    # connection.commit()

    # # Закрытие курсора и соединения
    # cursor.close()
    # connection.close()

    # print("Запись успешно добавлена в базу данных.")


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

