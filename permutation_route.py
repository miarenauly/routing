from time import time
import re
from os.path import exists
import sys
sys.path.append('library')
sys.path.append('core')
sys.path.append('models')
from sys import exit, argv
from time import sleep, strftime
from datetime import datetime
import json
import base64
from pgsqlib import *
from points_model import *
from gmaps_crawl import *
from pprint import pprint

def get_time():
    return datetime.today()
    
def first_permutation():
    qpoint = point_permutation()
    print (qpoint)
    rpoint = execScalar(qpoint)
    qpoint = del_depo_dest()
    print (qpoint)
    rpoint = execScalar(qpoint)
    print ("Doing First Permutation")
    
def second_permutation():
    qpoint = update_route_b()
    rpoint = execScalar(qpoint)
    print ("Doing Second Permutation")

def third_permutation():
    qpoint = update_route_c()
    rpoint = execScalar(qpoint)
    print ("Doing Third Permutation")

def update_engine(name):
    upd_ = updated_bot_name(name)
    execScalar(upd_)
    print ("Update To %s " %(name))

def data_crawl():
    bot_name = "engine_10093"
    update_engine(bot_name)
    qpoint = get_data_crawl(bot_name)
    rpoint = fetch(qpoint)
    for r in rpoint:
        idx = r[0]
        oid = r[1]
        olat = r[2]
        olon = r[3]
        did  = r[4]
        dlat = r[5]
        dlon = r[6]
        origin = "%s,%s" %(olat,olon)
        destination = "%s,%s" %(dlat,dlon)
        #print destination
        crawl_maps(origin,destination,oid,did)
        
        
def crawl_maps(origin,destination,oid,did):
    directions = google_direction(origin,destination)
    distance   = directions[0]["legs"][0]["distance"]["value"]
    polyline   = directions[0]["overview_polyline"]["points"]
    duration   = directions[0]["legs"][0]["duration"]["value"]
    time       = get_time()
    print (time)
    objects    = {
        "duration": duration,
        "distance": distance,
        "polyline": polyline,
        "time"    : time
    }
    
    upd_ = update_route_d(objects,oid,did)
    execScalar(upd_)
    pprint ("Update [%s][%s][D]" %(oid,did))

   
first_permutation()
second_permutation()
#data_crawl()
#third_permutation()