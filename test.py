
from googlemaps import Client
import psycopg2 #run export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib:$DYLD_FALLBACK_LIBRARY_PATH
from django.contrib.gis.geos import Point

#Connect to DB
try:
    conn = psycopg2.connect("dbname='mode' user='mms' host='localhost' password='001'")
except:
    print ("I am unable to connect to the database")

cur = conn.cursor()

#Initiate Google Maps services using "private" Token and Geocoder
mapService = Client('AIzaSyCy-F7kcigXdHaaAIFSH8DlfKe1Dl-aJOM')


#Execute SQL-Query to obtaind start and end points
try:
	cur.execute("""SELECT *
                    FROM vm.vm_od_max
                    WHERE vm_oid != vm_did""")
except:
    print('I cant SELECT from database')

vmidList = cur.fetchall()

try:
	cur.execute("""SELECT vmid,ST_Y(ST_TRANSFORM(node_geom,4326)),ST_X(ST_TRANSFORM(node_geom,4326))
                    FROM vm.vm_zones
                    ORDER BY vmid """)
except:
    print('I cant SELECT from database')

locationList = cur.fetchall()
time = 7
r =[]
#Loop through locations and fetch routes between all OD-pairs
for odPair in vmidList:
    for zone in locationList:
        if odPair[1] == zone[0]:
            start = zone[0]
            x = [zone[1], zone[2]]
        if odPair[2] == zone[0]:
            end = zone[0]
            y = [zone[1], zone[2]]

    directions = mapService.directions(
        x,
        y,
        'driving',
        None,
        True,
        None,
        None,
        None,
        None)

    #Add Each step of each route of each OD-pair
    print('start:', start, ' end: ', end)
    for routeIndex, route in enumerate(directions):
        for stepIndex, step in enumerate(route['legs'][0]['steps']):
            data = {'oid': start,
                    'did': end,
                    'route_index': routeIndex + 1,
                    'step_index': stepIndex + 1,
                    'start_point': Point(x[0], x[1]).wkt,
                    'end_point': Point(y[0], y[1]).wkt,
                    'dist': step['distance']['value'],
                    'tt': step['duration']['value']}
            r.append(data)

#Print all Routes
#for route in r:
#    print(route)

test3 = []
test3.append(r[0])
test3.append(r[0])
#print(test3)

#Add code to push routes to DB

try:
	cur.execute("""DELETE FROM vm.micke_test""")
	conn.commit()
except:
    print('Could not delete from DB')


try:
	cur.executemany("""INSERT INTO vm.micke_test(oid,did,route_index,step_index,start_point,end_point,dist,tt)
	VALUES (%(oid)s,%(did)s,%(route_index)s,%(step_index)s,%(start_point)s, %(end_point)s,%(dist)s,%(tt)s)""", r)
	conn.commit()
except:
    print ("Can't write to database")
