import psycopg2

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

except Exception as _ex:
    print('Exception occurred:', _ex)

