from googlemaps import Client
import psycopg2 #run export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib:$DYLD_FALLBACK_LIBRARY_PATH
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import fromstr
import psycopg2.extras

pnt = fromstr('POINT(-90.5 29.5)', srid=4326)

print(pnt.wkt)
