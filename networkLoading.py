import time
import dbUtil
import sys
import trafficAssignmentModel as TAM


user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil.dbConnect("'mode'", user, password)
time_periods = dbUtil.getTimePeriods(cur)


loop_limit = range(1, len(time_periods) + 1)
process_start_time = time.time()
for value in loop_limit:
    print(value)
    time_period = 1
    od_pairs = dbUtil.getDistinctOdRoutes(cur, conn, time_period)

    rows = len(od_pairs)
    test_rows = 0
    print('Assigning Traffic to ', rows, ' od-pairs')
    sys.stdout.write("\r%d%%" % ((0/rows*100)))

    for index,od in enumerate(od_pairs):

        sys.stdout.write("\r%d%%" % (((index + 1)/rows*100)))
        routes = dbUtil.getOdRoutes(cur, conn, od, time_period)
        test_rows = test_rows + len(routes)
        shares = TAM.getRouteShares(routes)


process_elapsed_time = time.time() - process_start_time
print('')
print('Process done in: ', process_elapsed_time, 's')
print(test_rows)
