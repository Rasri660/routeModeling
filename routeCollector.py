import dbUtil
import googleRoutes


#Connect to DB
user = input('User: ')
password = input('Password: ')

user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil.dbConnect("'mode'", user, password)

print(cur, conn)
#Fetch data from db
time_periods = dbUtil.getTimePeriods(cur)
node_list = dbUtil.getNodeList(cur)
od_list = dbUtil.getOdList(cur)

#Start collecting routes from Google
time_period = 1

routes = googleRoutes.getGoogleRoutes(od_list, node_list, time_period)

dbUtil.deleteRoutes(cur, conn)
dbUtil.storeRoutes(cur, conn, routes)
