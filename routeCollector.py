import time
import dbUtil
import googleRoutes

#Connect to DB
#user = input('User: ')
#password = input('Password: ')

user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil.dbConnect("'mode'", user, password)

print('\n')

#Fetch data from db
start_time = time.time()

time_periods = dbUtil.getTimePeriods(cur)
elapsed_time = time.time() - start_time
print('Time periods collected in: ', elapsed_time, 'ms')
start_time = time.time()

node_list = dbUtil.getNodeList(cur)
elapsed_time = time.time() - start_time
print('Nodes collected in: ', elapsed_time, 'ms')
start_time = time.time()

od_list = dbUtil.getOdList(cur)
elapsed_time = time.time() - start_time
print('OD relations collected in: ', elapsed_time, 'ms')
start_time = time.time()

#Start collecting routes from Google
time_period = 6
print('Route extraction initialised')
routes = googleRoutes.getGoogleRoutes(od_list, node_list, time_period, time_periods)
print(routes)
print(' ')
print('Route extraction complete!')

#dbUtil.deleteRoutes(cur, conn)
#dbUtil.storeRoutes(cur, conn, routes)
