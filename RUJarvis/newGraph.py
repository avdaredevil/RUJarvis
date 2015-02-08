from networkx import *
import networkx as nx
import json
from pprint import pprint
import simplejson, urllib
import json
from pygeocoder import Geocoder
import requests

#open json file
json_data = open ('Redirecting.json')
data = json.load(json_data)

def gettime(f_lat, f_lon, s_lat, s_lon):
	ap_api_key = "AuhAQe-eO4hV_5ngO8fui3TM_eIKTRXUwGQH4IA-62-9zPjBDIQh13aJnDom3wR3"
	ap_result = requests.get("http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0="+str(f_lat)+" "+str(f_lon)+"&wp.1="+str(s_lat)+" "+str(s_lon)+"&du=mi&key="+ap_api_key)
	return (ap_result.json())['resourceSets'][0]['resources'][0]['travelDuration']

def makeDiGraph():
	DG = nx.DiGraph()
	stop_hash= {}
	for stops in data["stops"]:
		temp = data["stops"][stops]
		stop_hash[stops] = {"title":temp['title'], "lat":temp['lat'], "lon":temp['lon'], "routes":temp['routes']}
		DG.add_node(stops)

	#read edge weights
	bus_routes = ["a", "b", "c", "ee", "f", "h", "lx", "rexb", "rexl", "wknd1", "wknd2"]
	for routes in bus_routes:
		temp = data["routes"][routes]
		for i in range(len(temp['stops'])):
			first_stop = temp['stops'][i]
			second_stop = temp['stops'][(i+1)%len(temp['stops'])]
			first_lat = data['stops'][first_stop]["lat"]
			first_lon = data['stops'][first_stop]["lon"]
			second_lat = data['stops'][second_stop]["lat"]
			second_lon =  data['stops'][second_stop]["lon"]
			weight_edge = gettime(first_lat, first_lon, second_lat, second_lon)
			DG.add_edge(first_stop,second_stop, weight= weight_edge)	
	return DG

def findroutes(DG, init_dest, final_dest):
	num = 0
	count =1
	while(num < 4):
		paths = all_simple_paths(DG, init_dest, final_dest,count)
		path_mod = list(path)
		num = len(path_mod)
		count= count+1
	return path_mod		

def calculate_optimum_path(paths):
        time = 0
        first = 0
        second = 1
        length = len(paths)
        for x in range(0,length):
                curr_path = paths[x]
                for y in range(0,length-1):
                        first_stop = curr_path[y]
                        common_busses = set(first_stop).intersection(curr_path[y+1])
                        for z in range(0,len(common_busses)):
                                next_bus(first_stop, common_busses)
                        #final_busses = set(data["stops"][curr_path[y]]['routes']).intersection(common_busses)



def get_best_path(init_dest, final_dest):
	DG = makeDiGraph()
        paths = findroutes(DG, init_dest, final_dest) 


if __name__ == "__main__":
	init_dest = "hilln"
	final_dest = "scott"
	get_best_path(init_dest, final_dest)
