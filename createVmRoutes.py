#createVmRoutes
import dbUtil

user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil.dbConnect("'mode'", user, password)

print('Creating VM-routes')
routes = dbUtil.createVmRoutes(cur, conn)
print('Process complete!')


# for index, route in enumerate(routes):
#     elapsed_time = time.time() - start_time
#     if elapsed_time >= 1:
#         sys.stdout.write("\r%d%%" % ((index/len(routes)*100)))
#         sys.stdout.flush()
#
#     route_id = route[1]
#     geom = dbUtil.createRouteGeom(cur, conn, route_id)
#     geom = geom[0][1]
#     dbUtil.insertRouteGeom(cur, conn, geom, route_id)
