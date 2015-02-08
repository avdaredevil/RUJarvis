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

lookup = { "Weekend 1":"wknd1" , "Weekend 2":"wknd2" , "A": "a", "B": "b", "REX L" :"rexl", "REX B": "rexb", "LX" : "lx" , "H": "h", "F":"f" }

def makeDiGraph():
    # Init Graph
    DG = nx.Graph()
    #create all nodes for the graph initilized with the following values
    for stops in data["stops"]:
        DG.add_node(stops)
        #DG[stops]['title'] = data["stops"][stops]['title']
        #DG[stops]['lat'] = data["stops"][stops]['lat']
        #DG[stops]['lon'] = data["stops"][stops]['lon']
        #DG[stops]['routes'] = data["stops"][stops]['routes']
    #read edge weights
    weights = []
    f = open("durations.txt", 'r')
    for line in f:
        weights.append(int(line))
        
    #print len(weights)
    #create the edges for each route 
    sum = 0
    for routes in data["routes"]:
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
    if init_stop not in data["stops"]:
        return "BIG Fail"
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
 
def getTitle(DG, dest):
    for stops in DG:
        if(stops["title"] == dest):
            return stops['title']
    return 0        

'''
def total_time(a, origin, activeroutes):
    url = "http://runextbus.heroku.com/stop/{0}".format(str(origin))
    time = simplejson.load(urllib.urlopen(url))
    t = 0;
    for items in time:
        for routes in a: 
            if lookup[items['title']] == routes):
                for n in items["predictions"]:
                    print n["seconds"]
                    t = t + n["seconds"]
                    break     
    
    for routes in a:
        overhead = a + t
    print time
    return  
'''

def get_best_path (init_dest, final_dest):
    DG = makeDiGraph()
    x= findCommonRoutes(init_dest, final_dest, DG)
    # check if any common bus is active
    activeRoutes = isActive(x)
    if(len(activeRoutes) == 0):
        print "You are fucked, buddy. No active routes"
    else: 
        # TOTAL TIME incomplete !!   
        best = (nx.bidirectional_dijkstra(DG, init_dest, final_dest , weight = 'edge_weight') )
        return activeRoutes,best

if __name__ == "__main__":
    
    '''
    #main 
    DG = makeDiGraph()
    #print DG['scott']['stuactcntr'].get('edge_weight',1)

    
    #take input data
    in_lat =40.49957
    in_lon =-74.44824
    fi_lat = 40.491856 
    fi_lon = -74.4430933
    init_dest = closest_stops(in_lat, in_lon)
    final_dest = closest_stops(fi_lat, fi_lon ) 
    
    

    #FIND COMMON buses between two stops (not including no common buses between init and final)
    x= findCommonRoutes(init_dest, final_dest, DG)
    # check if any common bus is active
    activeRoutes = isActive(x)
    if(len(activeRoutes) == 0):
        print "You are fucked, buddy. No active routes"
    else: 
        print activeRoutes
        # TOTAL TIME incomplete !!   
        best = (nx.bidirectional_dijkstra(DG, init_dest, final_dest , weight = 'edge_weight') )
        print (best)
    '''       
    init_dest = "hilln"
    final_dest = "scott" 
    get_best_path(init_dest, final_dest)    








