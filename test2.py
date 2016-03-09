from googlemaps import Client
import psycopg2 #run export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib:$DYLD_FALLBACK_LIBRARY_PATH
from django.contrib.gis.geos import Point
import psycopg2.extras

try:
    conn = psycopg2.connect("dbname='mode' user='mms' host='localhost' password='001'")
except:
    print ("I am unable to connect to the database")

cur = conn.cursor()

test = ({'oid': 8, 'did': 22, 'route_index': 1, 'step_index': 1, 'start_point': 'hej', 'end_point': 'da', 'dist': 727, 'tt': 84},
        {'oid': 9, 'did': 23, 'route_index': 1, 'step_index': 1, 'start_point': 'hej', 'end_point': 'da', 'dist': 727, 'tt': 84})

try:
	cur.executemany("""INSERT INTO vm.micke_test (oid, did, route_index, step_index, start_point, end_point, dist, tt)
                        VALUES(%(oid)s, %(did)s, %(route_index)s, %(step_index)s, %(start_point)s, %(end_point)s, %(dist)s, %(tt)s""", test)
	conn.commit()
except:
    print ("Did not insert to database")
