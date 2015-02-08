import simplejson, urllib
import json
from pygeocoder import Geocoder
json_data= open("Redirecting.json")
data = json.load(json_data)
f = open('togive.txt', "r")
k = open('durations2.txt', "w")
count = 1
for line in f:
    if(count <= 163):
        count= count +1
        continue
    x = line.split()
    results1 = Geocoder.reverse_geocode(float(x[0]), float(x[1]))
    orig_coord = results1[0]
    results2 = Geocoder.reverse_geocode(float(x[2]),float(x[3]))
    dest_coord = results2[0]
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
    result= simplejson.load(urllib.urlopen(url))
    driving_time = result['rows'][0]['elements'][0]['duration']['value']
    print driving_time
    k.write(str(driving_time))
    k.write('\n')
