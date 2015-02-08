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

