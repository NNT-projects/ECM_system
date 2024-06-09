import psycopg2
from params_for_DB import *
import pandas as pd


def update_database_from_dataframe(dataframe: pd.DataFrame):
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            host=host,
            password=password,
            port=port
        )
        cursor = connection.cursor()

        for index, row in dataframe.iterrows():
            reportts = row['reportts'].strftime('%Y-%m-%d %H:%M:%S')
            acnum = row['acnum']
            pos = str(row['pos'])

            cursor.execute(
                f"SELECT * FROM {table_name} WHERE reportts = %s AND acnum = %s AND pos = %s",
                (reportts, acnum, pos))
            existing_record = cursor.fetchone()

            if existing_record:
                egtm = str(row['egtm'])
                cursor.execute(
                    f"UPDATE {table_name} SET egtm = %s WHERE reportts = %s AND acnum = %s AND pos = %s",
                    (egtm, reportts, acnum, pos))
            else:
                sql = f"INSERT INTO {table_name} ({', '.join(dataframe.columns)}) VALUES ({', '.join(['%s'] * len(row))})"
                cursor.execute(sql, tuple(row))

        connection.commit()
        connection.close()
        cursor.close()
    except Exception as _ex:
        print("Exception while updating database:", _ex)
