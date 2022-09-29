import requests
import pandas as pd


prof_role = "data+engineer"
headers = {"User-Agent": "api-test-agent"}

try:
    r = requests.get("https://api.hh.ru/vacancies?text={search}&per_page=30".format(search=prof_role), headers=headers)
    data = r.json()
except:
    raise Exception("Data didn't load")

# Normalizing data
flat_table = pd.json_normalize(data, record_path=['items'])

# Saving to CSV file
flat_table.to_csv('vacancies_data_engineer.csv')

# print(flat_table)
