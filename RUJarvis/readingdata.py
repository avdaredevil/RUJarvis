import json
json_data = open ('Redirecting.json')
data = json.load(json_data)
f = open('workfile', 'r')

k = open('togive.txt', 'w')

for line in f:
    x = line.split()
    stop1 = x[0]
    stop2 = x[1]
    k.write(data["stops"][stop1]['lat'] + " " + data["stops"][stop1]['lon'] + " " + data["stops"][stop2]['lat'] + " " + data["stops"][stop2]['lon'])
    k.write('\n')
    
