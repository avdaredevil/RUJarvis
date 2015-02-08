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

lookup_bus = { "Weekend 1":"wknd1" , "Weekend 2":"wknd2" , "A": "a", "B": "b", "REX L" :"rexl", "REX B": "rexb", "LX" : "lx" , "H": "h", "F":"f" }
lookup_stops = { "Library of Science": "libofsci" , "Visitor Center": "lot48a" , "Scott Hall": "scott" , "Train Station": "traine_a" , "College Hall": "college_a" , "Cabaret Theatre": "cabaret" , "Busch Campus Center": "busch" , "Allison Road Classrooms": "allison_a" , "Busch Campus Center": "busch_a" , "Hill Center": "hillw" , "Red Oak Lane": "redoak_a" , "Library of Science": "libofsciw" , "Bravo Supermarket": "newstree" , "Busch Suites": "buschse" , "Student Activities Center": "stuactcntrs" , "Nursing School": "nursscho" , "Zimmerli Arts Museum": "zimmerli_2" , "Liberty Street": "liberty" , "Gibbons": "gibbons" , "Biel Road": "biel" , "Livingston Student Center": "livingston_a" , "Katzenbach": "katzenbach" , "Student Activities Center": "stuactcntrn" , "Hill Center": "hilln" , "Rockoff Hall": "rockhall" , "Davidson Hall": "davidson" , "Paterson Street": "patersons" , "Rutgers Student Center": "rutgerss" , "College Hall": "college" , "Lipman Hall": "lipman" , "Quads": "quads" , "Colony House": "colony" , "Henderson": "henders" , "Stadium": "stadium_a" , "Livingston Plaza": "beck" , "Werblin Back Entrance": "werblinback" , "Red Oak Lane": "redoak" , "Zimmerli Arts Museum": "zimmerli" , "Student Activities Center": "stuactcntrn_2" , "Food Sciences Building": "foodsci" , "Rutgers Student Center": "rutgerss_a" , "Train Station": "traine" , "Paterson Street": "patersonn" , "Student Activities Center": "stuactcntr" , "Science Building": "science" , "Werblin Main Entrance": "werblinm" , "Public Safety Building South": "pubsafs" , "Rockoff Hall": "rockoff" , "Allison Road Classrooms": "allison" , "Livingston Student Center": "livingston" , "Train Station": "trainn_a" , "Buell Apartments": "buells" , "Public Safety Building North": "pubsafn" , "Buell Apartments": "buel" , "Train Station": "trainn" }



def makeDiGraph():
    # Init Graph
    DG = nx.Graph()
    stop_hash = {}
    #create all nodes for the graph initilized with the following values
    for stops in data["stops"]:
	temp = data["stops"][stops]
	stop_hash[stops] = {"title":temp['title'], "lat":temp['lat'], "lon":temp['lon'], "routes":temp['routes']}
        DG.add_node(stops)

    #read edge weights
    weights = []
    f = open("durations.txt", 'r')
    for line in f:
        weights.append(int(line))

    #print len(weights)
    #create the edges for each route
    sum = 0
    for routes in data["routes"]:
	temp = data["routes"][routes] 
        for i in range( len(data["routes"][routes]['stops'])):
            DG.add_edge(data["routes"][routes]['stops'][i], data["routes"][routes]['stops'][(i+1)%len(data["routes"][routes]['stops'])],edge_weight = weights[sum])
            sum = sum +1
    return DG


def isExisting(s):
    for stops in data["stops"]:
        if(s == data["stops"][stops]['title']):
            return stops
    return 0

def closest_stops(x,y):
    # input user data
    url = "http://runextbus.heroku.com/nearby/{0}/{1}".format(str(x),str(y))
    result = simplejson.load(urllib.urlopen(url))
    min = 100
    k = []
    for stops in result:
        k.append(stops)
    return k

def findCommonRoutes(init_stop, final_stop, DG):
    result = []
    for route in data["stops"][init_stop]["routes"]:
        for routes in data["stops"][final_stop]["routes"]:
            if (route == routes):
                result.append("s")
                result.append(route)

    if (len(result) == 0):
        #here is where the depth first search begins
        p = nx.all_shortest_paths(DG, init_stop, final_stop)
        print p
    return result


def isActive(x):
    url = "http://runextbus.heroku.com/active"
    common_buses = []
    active = simplejson.load(urllib.urlopen(url))
    for routes in active["routes"]:
        for route in x:
            #print routes["tag"]
            #print route
            if(routes["tag"] == route):
                common_buses.append(route)
    return common_buses

def next_bus (origin, a):
    url = "http://runextbus.heroku.com/stop/{0}".format(str(origin))
    time = simplejson.load(urllib.urlopen(url))
    t = 0;
    for items in time:
        if items['predictions'] != None:
            for routes in a:
                if lookup_bus[str(items['title'])] == routes:
                    print lookup_bus[str(items['title'])]
                    print routes
                    for n in items['predictions']:
                        t = n["seconds"]
                        break
    return t
    
    
def total_time(a, origin, activeroutes):
    t = next_bus (origin, activeroutes)
    print activeroutes
    print t
    return

def get_best_path (init_dest, final_dest):
    DG = makeDiGraph()
    x= findCommonRoutes(init_dest, final_dest, DG)
    # check if any common bus is active
    activeRoutes = isActive(x)
    if(len(activeRoutes) == 0):
        print "You are fucked, buddy. No active routes"
    else:
        print activeRoutes
        # TOTAL TIME incomplete !!
        total_time(x,init_dest, activeRoutes)
        best = (nx.bidirectional_dijkstra(DG, init_dest, final_dest , weight = 'edge_weight') )
        print (best)

if __name__ == "__main__":

    init_dest = "hilln"
    final_dest = "scott"
    get_best_path(init_dest, final_dest)








