#==========================Imports==========|
from __future__ import absolute_import
import networkx as nx
import urllib,requests,time
try: import simplejson as json
except ImportError: import json
from networkx import *
from pygeocoder import Geocoder
from networkx.readwrite import json_graph
#==========================Imports=====END==|

#open json file
json_data = open ('data/Redirecting.json')
data = json.load(json_data)

lookup_bus = { "Weekend 1":"wknd1" , "Weekend 2":"wknd2" , "A": "a", "B": "b", "C": "c", "REX L" :"rexl", "REX B": "rexb", "LX" : "lx" , "H": "h", "F":"f","EE":"ee","New Brunsquick 1 Shuttle":"w1","New Brunsquick 2 Shuttle":"w2"}
lookup_stops = { "Library of Science": "libofsci" , "Visitor Center": "lot48a" , "Scott Hall": "scott" , "Train Station": "traine_a" , "College Hall": "college_a" , "Cabaret Theatre": "cabaret" , "Busch Campus Center": "busch" , "Allison Road Classrooms": "allison_a" , "Busch Campus Center": "busch_a" , "Hill Center": "hillw" , "Red Oak Lane": "redoak_a" , "Library of Science": "libofsciw" , "Bravo Supermarket": "newstree" , "Busch Suites": "buschse" , "Student Activities Center": "stuactcntrs" , "Nursing School": "nursscho" , "Zimmerli Arts Museum": "zimmerli_2" , "Liberty Street": "liberty" , "Gibbons": "gibbons" , "Biel Road": "biel" , "Livingston Student Center": "livingston_a" , "Katzenbach": "katzenbach" , "Student Activities Center": "stuactcntrn" , "Hill Center": "hilln" , "Rockoff Hall": "rockhall" , "Davidson Hall": "davidson" , "Paterson Street": "patersons" , "Rutgers Student Center": "rutgerss" , "College Hall": "college" , "Lipman Hall": "lipman" , "Quads": "quads" , "Colony House": "colony" , "Henderson": "henders" , "Stadium": "stadium_a" , "Livingston Plaza": "beck" , "Werblin Back Entrance": "werblinback" , "Red Oak Lane": "redoak" , "Zimmerli Arts Museum": "zimmerli" , "Student Activities Center": "stuactcntrn_2" , "Food Sciences Building": "foodsci" , "Rutgers Student Center": "rutgerss_a" , "Train Station": "traine" , "Paterson Street": "patersonn" , "Student Activities Center": "stuactcntr" , "Science Building": "science" , "Werblin Main Entrance": "werblinm" , "Public Safety Building South": "pubsafs" , "Rockoff Hall": "rockoff" , "Allison Road Classrooms": "allison" , "Livingston Student Center": "livingston" , "Train Station": "trainn_a" , "Buell Apartments": "buells" , "Public Safety Building North": "pubsafn" , "Buell Apartments": "buel" , "Train Station": "trainn" }

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
			f_lat = data['stops'][first_stop]["lat"]
			f_lon = data['stops'][first_stop]["lon"]
			s_lat = data['stops'][second_stop]["lat"]
			s_lon = data['stops'][second_stop]["lon"]
			api_ct = 3
			while api_ct > 0:
				--api_ct
				try: weight_edge = gettime(f_lat, f_lon, s_lat, s_lon)
				except (ValueError,IndexError): time.sleep(.5);continue
				break
			if api_ct == 0: raise AP_API_Fail
			DG.add_edge(first_stop,second_stop, weight= weight_edge)	
	return DG

def findroutes(DG, init_dest, final_dest):
	num = 0
	count = 1
	while(num < 4):
		paths = all_simple_paths(DG, init_dest, final_dest,count)
		path_mod = list(paths)
		num = len(path_mod)
		count= count+1
	return path_mod		

def calculate_optimum_path(DG,paths):
	super_min = 10000000;first = 0
	second = 1
	best_path = []
	for x in range(0,len(paths)-1):
		try:
			curr_path = paths[x];ETA = 0
			best_all = []
			for y in range(0,len(curr_path)-2):
				curr_stop = curr_path[y]
				common_busses = set(AP_BusesAt(curr_stop)).intersection(set(AP_BusesAt(curr_path[y+1])))
				bus = ap_best_bus(curr_stop,common_busses,ETA)
				print "Predictions beyond accurate scope!"
				if not bus: raise StopIteration
				max_ap = ETA = float(bus['time'])#+DG[curr_stop][curr_path[y+1]]['weight'] --AP -Not sure why you needed this
				if super_min<ETA: raise StopIteration
				best_all.append(bus)
				#final_busses = set(data["stops"][curr_path[y]]['routes']).intersection(common_busses)
			if super_min > ETA: super_min = ETA;best_path = best_all
		except StopIteration: pass
#	last_stop = ap_best_bus(curr_path[-1],set(best_path[-1]['bus']),super_min)
#	best_path.append(last_stop);super_min+=last_stop['time']
	return {'Stops': best_path,'Time': super_min}

def AP_BusesAt(stop):
	return data['stops'][stop]['routes']

def ap_best_bus(stop,buses,durationAt=0):
	url = "http://runextbus.heroku.com/stop/{0}".format(str(stop))
	res = json.load(urllib.urlopen(url));minb = {}
	for bus in res:
		if not bus['predictions'] or not lookup_bus[bus['title']] in buses: continue
		print "Comparing "+str("true" if not minb else minb['time'])+" > "+str(fetchMinPred(bus['predictions'],durationAt))
		if (not minb or minb['time'] > fetchMinPred(bus['predictions'],durationAt)): minb = {'bus': lookup_bus[bus['title']], 'stop': stop, 'time': int(float(bus['predictions'][0]['seconds']))}
	return minb if minb and minb['time']>durationAt else {}

def fetchMinPred(preds, DAT):
	for p in preds:
		if int(float(p['seconds']))>DAT: return int(float(p['seconds']))
	return 100000

def get_best_path(init_dest, final_dest):
#	DG = makeDiGraph()
#	SaveGraph(DG, "data/ap_graph.json")
	DG = LoadGraph("data/ap_graph.json")
	paths = findroutes(DG, init_dest, final_dest) 
	best_path = calculate_optimum_path(DG,paths)
	return json.dumps(best_path);

def SaveGraph(G, fname):
	json.dump(dict(nodes=[[n, G.node[n]] for n in G.nodes()],edges=[[u, v, G.edge[u][v]] for u,v in G.edges()]),open(fname, 'w'), indent=2)

def LoadGraph(fname):
	G = nx.DiGraph()
	d = json.load(open(fname))
	G.add_nodes_from(d['nodes'])
	G.add_edges_from(d['edges'])
	return G

if __name__ == "__main__":
	init_dest = "hilln"
	final_dest = "scott"
	best_path = get_best_path(init_dest, final_dest)
	print best_path
