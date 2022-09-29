import pandas as pd
import re
import json


with open('raw_interface_data.txt') as file:
    src = file.read()

sys_name = re.findall(r'System Name: \w+.\w+', src)
clear_system_name = sys_name[0].replace('System Name: ', '' )

file = open('raw_interface_data.txt', 'r')
lines = file.readlines()
dict = []
for line in lines:
    dict.append(line.replace('\\r', '').replace('\n', '').replace("'", '').strip())

table = []
c = 0
for l in dict:
    if l == '':
        c += 1
        continue
    if c == 1 and l != '':
        table.append(l)

json_data = []

# headers = table[1:2][0].split(' ')
headers = ('Port_1', 'Port_2', 'Mode', 'State_1', 'State_2', 'Description')

data = table[3:]

for l in range(len(data)):
    a = data[l].split(' ')
    json_data.append({})
    for i in range(len(a)):
        json_data[l].update({headers[i]: a[i]})
    json_data[l].update({'System Name': clear_system_name})

fl =  open('json_interfase_data.json', 'w')
json.dump(json_data, fl)