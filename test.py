import csv
from typing import List

csv_file_path = 'C:/Users/pengv/Downloads/X_train.csv'
table_name = 'data_engine'

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
    print(columns)