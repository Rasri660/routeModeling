
from googlemaps import Client
from pygeocoder import Geocoder
import psycopg2

#Connect to DB
try:
    conn = psycopg2.connect("dbname='mode' user='mms' host='localhost' password='001'")
except:
    print ("I am unable to connect to the database")

cur = conn.cursor()

#Initiate Google Maps services using "private" Token and Geocoder
mapService = Client('AIzaSyCy-F7kcigXdHaaAIFSH8DlfKe1Dl-aJOM')
geocoder = Geocoder()


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

for odPair in vmidList:
    for zone in locationList:
        if odPair[1] == zone[0]:
            x = geocoder.reverse_geocode(zone[1], zone[2])
        if odPair[2] == zone[0]:
            y = geocoder.reverse_geocode(zone[1], zone[2])

    directions = mapService.directions(
    x.coordinates,
    y.coordinates,
    'driving',
    None,
    True)

print('start:', test1.coordinates, ' end: ', test2.coordinates)
for routeIndex, route in enumerate(directions):
    print('Route: ', routeIndex + 1)

    for step in route['legs'][0]['steps']:
        print(step['start_location'], step['distance'], step['duration'])
