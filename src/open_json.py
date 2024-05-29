import json
import pandas as pd

#получение json
with open('../data/response2.json', 'r') as json_file:
    data = json.load(json_file)

# print(data)

df = pd.DataFrame(data)

print(df)