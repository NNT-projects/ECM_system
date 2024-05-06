import psycopg2
from params_for_DB import *


from psycopg2 import sql

def update_database_from_dataframe(df, table_name):
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        host=host,
        password=password,
        port=port
    )
    cursor = connection.cursor()

    for index, row in df.iterrows():
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        query = sql.SQL("UPDATE {} SET ({}) = ({}) WHERE id = %s").format(
            sql.Identifier(table_name),
            sql.SQL(columns),
            sql.SQL(placeholders)
        )
        values = tuple(row) + (row['id'],)
        cursor.execute(query, values)
        connection.commit()

    cursor.close()
    connection.close()