from networkx import *
import networkx as nx
import json
from pprint import pprint
import simplejson, urllib
import json
from pygeocoder import Geocoder

#open json file
json_data = open ('Redirecting.json')
data = json.load(json_data)

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

			DG.add_edge(first_stop,second_stop)
	return DG



def findroutes(DG, init_dest, final_dest):
	num = 0
	count =1
	while(num < 4):
		paths = all_simple_paths(DG, init_dest, final_dest,count)
		path_mod = list(path)
		num = len(path_mod)
		count= count+1
		
	
	
def get_best_path():
	DG = makeDiGraph()


if __name__ == "__main__":
	init_dest = "hilln"
	final_dest = "scott"
	get_best_path(init_dest, final_dest)
