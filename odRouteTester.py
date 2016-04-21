import time
import dbUtil
import googleRoutes
from datetime import datetime

#Connect to DB
#user = input('User: ')
#password = input('Password: ')

user = 'vm-user'
password = '001'

user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil.dbConnect("'mode'", user, password)

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

od_list = dbUtil.getOdListTEST(cur)
elapsed_time = time.time() - start_time
print('OD relations collected in: ', elapsed_time, 'ms')
start_time = time.time()

time_period = 12
print('Route extraction initialised')
routes = googleRoutes.getGoogleRoutes(od_list, node_list, time_period, time_periods)
print(' ')
print('Route extraction complete, inserting into DB')

dbUtil.storeRoutes(cur, conn, routes)

print('Process complete!')
