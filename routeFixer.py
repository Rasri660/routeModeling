import dbUtil_routeFixer


user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil_routeFixer.dbConnect("'mode'", user, password)

#distinct_routes = dbUtil_routeFixer.getUniqueRoutes(cur, conn)

data = dbUtil_routeFixer.getRouteStepLinks(cur, conn, '1077:1:1')

for i in data:
    print(i)
