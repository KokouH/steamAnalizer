
import  json

s = input("Copy cookies from browser: ")

s = s.split('; ')
s = [i.split('=') for i in s]
c = {}

for  i in s:
    c[i[0]] = i[1]

with open("cookies.json", 'w') as file:
    file.write(json.dumps(c))