#createVmRoutes
import time
import dbUtil
import sys
#import os


user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil.dbConnect("'mode'", user, password)

routes = dbUtil.getGoogleRoutes(cur, conn)

start_time = time.time()
counter = 0

sys.stdout.write("\r%d%%" % (0))
sys.stdout.flush()

for index, route in enumerate(routes):

    if index > 100:
        break


    elapsed_time = time.time() - start_time
    if elapsed_time >= 1:
        sys.stdout.write("\r%d%%" % ((index/len(routes)*100)))
        sys.stdout.flush()

    route_id = route[1]
    geom = dbUtil.createRouteGeom(cur, conn, route_id)
    geom = geom[0][1]
    dbUtil.insertRouteGeom(cur, conn, geom, route_id)
