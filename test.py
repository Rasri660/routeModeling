
from googlemaps import Client
import time
import psycopg2 #run export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib:$DYLD_FALLBACK_LIBRARY_PATH
from django.contrib.gis.geos import Point
from datetime import datetime

#Connect to DB
try:
    conn = psycopg2.connect("dbname='mode' user='mms' host='localhost' password='001'")
except:
    print ("I am unable to connect to the database")

cur = conn.cursor()

#Initiate Google Maps services using "private" Token and Geocoder
mapService = Client('AIzaSyCy-F7kcigXdHaaAIFSH8DlfKe1Dl-aJOM')


#QUERY to extract all OD-relations where routes shall be extracted from google.
try:
	cur.execute("""SELECT od_id, vm_oid, vm_did
                    FROM vm.vm_od_max
                    WHERE (vm_oid = 8)""")
except:
    print('I cant SELECT from database')

vmidList = cur.fetchall()

#Query to get start and end points for all vm_zones
try:
	cur.execute("""SELECT vmid,ST_Y(ST_TRANSFORM(node_geom,4326)),ST_X(ST_TRANSFORM(node_geom,4326))
                    FROM vm.vm_zones
                    ORDER BY vmid """)
except:
    print('I cant SELECT from database')


locationList = cur.fetchall()

time_period = 1
test_time = datetime(2016,9,6,6,30,0)
r =[]


#Loop through locations and fetch routes between all OD-pairs
for odPair in vmidList:
    for zone in locationList:
        if odPair[1] == zone[0]:
            #start = zone[0]
            x = [zone[1], zone[2]]
        if odPair[2] == zone[0]:
            #end = zone[0]
            y = [zone[1], zone[2]]

    # print(odPair[0])
    # print(x,y)


    directions = mapService.directions(
        x,
        y,
        'driving',
        None,
        True,
        None,
        None,
        None,
        None,
        test_time)
    #print(directions[0]['legs'][0]['steps'][0]['start_location'], directions[0]['legs'][0]['steps'][0]['end_location'])
    #Add Each step of each route of each OD-pair
    #print('start:', start, ' end: ', end)
    for routeIndex, route in enumerate(directions):
        for stepIndex, step in enumerate(route['legs'][0]['steps']):
            data = {'od_id': odPair[0],
                    'route_id': str(odPair[0]) + ':' + str(routeIndex + 1) + ':' + str(time_period),
                    'start_point': Point(step['start_location']['lng'], step['start_location']['lat']).wkt,
                    'end_point': Point(step['end_location']['lng'], step['end_location']['lat']).wkt,
                    'route_index': routeIndex + 1,
                    'step_index': stepIndex + 1,
                    'travel_time': step['duration']['value'],
                    'distance': step['distance']['value'],
                    'time_period': time_period,
                    'time_stamp': test_time.strftime("%Y-%m-%d %H:%M:%S")}

            r.append(data)
#Print all Routes
# for route in r:
#   print(route)

#Add code to push routes to DB
try:
	cur.execute("""DELETE FROM vm.micke_test""")
	conn.commit()
except:
    print('Could not delete from DB')

try:
	cur.executemany("""INSERT INTO vm.micke_test (od_id, route_id, start_point, end_point, route_index, step_index, travel_time, distance, time_period) VALUES (%(od_id)s, %(route_id)s, %(start_point)s, %(end_point)s, %(route_index)s, %(step_index)s, %(travel_time)s, %(distance)s, %(time_period)s)""", r)
#,%(route_id)s,%(start_point)s,%(end_point)s,%(route_index)s, %(step_index)s,%(travel_time)s,%(distance)s),%(time_period)s)""", r)

	conn.commit()
except:
    print ("Can't write to database...")
