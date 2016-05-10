import time
import dbUtil
import sys
from polyline.codec import PolylineCodec
from django.contrib.gis.geos import Point
import googleRoutes
import polyDecode
#import os

#os.system('export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib:$DYLD_FALLBACK_LIBRARY_PATH')



user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil.dbConnect("'mode'", user, password)

distinct_routes = dbUtil.getDistinctStepsCoordinates(cur, conn)

steps = []
#a = [2422, 2354]
for index, route in enumerate(distinct_routes):
    steps.append(route[0])

start_time = time.time()
print('Creating Polyline for: ', len(steps), 'Unique steps')
sys.stdout.write("\r%d%%" % ((0/len(steps)*100)))

for index, i in enumerate(steps):

    if index >= 2000:

        data = []
        x = [distinct_routes[i][2], distinct_routes[i][1]]
        y = [distinct_routes[i][4], distinct_routes[i][3]]

        polyline = googleRoutes.getGooglePolyline(x,y)
        decoded_polyline = PolylineCodec().decode(polyline)

        for sequence_number, line in enumerate(decoded_polyline):
            data.append([distinct_routes[i][0], sequence_number, Point(line[1], line[0]).wkt])

        data[0] = [distinct_routes[i][0], 0, Point(x[1], x[0]).wkt]
        data[len(data) - 1] = [distinct_routes[i][0], len(data) - 1, Point(y[1], y[0]).wkt]

        dbUtil.storeUniqueStepsPolly(cur, conn, data)

    sys.stdout.write("\r%d%%" % ((index/len(steps)*100)))
    sys.stdout.flush()
