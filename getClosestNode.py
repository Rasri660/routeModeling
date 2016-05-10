import time
import dbUtil
import sys
#import os

#os.system('export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib:$DYLD_FALLBACK_LIBRARY_PATH')

user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil.dbConnect("'mode'", user, password)

distinct_routes = dbUtil.getDistinctSteps(cur, conn)

lines = []
start_time = time.time()
counter = 0

print('Createing: ', len(distinct_routes), ' unique steps')
for index, route in enumerate(distinct_routes):
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1:
        sys.stdout.write("\r%d%%" % ((counter/len(distinct_routes)*100)))
        sys.stdout.flush()

    start = route[0]
    end = route[1]
    start_info = dbUtil.getClosestSource(cur, conn, start)
    end_info = dbUtil.getClosestTarget(cur, conn, end)

    start_node = start_info[0][0]
    end_node = end_info[0][0]
    start_dist = start_info[0][2]
    end_dist = end_info[0][2]
    start_link = start_info[0][3]
    end_link = end_info[0][3]

    if(start_dist < 1000 and end_dist < 1000):
        lines.append((index, start_link, start_node, start_dist, end_link, end_node, end_dist, start, end))

    counter = counter + 1

dbUtil.storeUniqueStepsTest(cur, conn, lines)
