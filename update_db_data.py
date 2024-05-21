import psycopg2
from params_for_DB import *

from io import StringIO


def update_database_from_dataframe(dataframe):
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        host=host,
        password=password,
        port=port
    )
    cursor = connection.cursor()

    buffer = StringIO()
    dataframe.to_csv(buffer, header=False, index=False, sep='\t')
    buffer.seek(0)

    cursor.copy_from(buffer, table_name, columns=dataframe.columns, sep='\t')
    connection.commit()

    cursor.close()
    connection.close()
