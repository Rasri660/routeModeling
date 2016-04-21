import time
import dbUtil
import sys
#import os

#os.system('export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib:$DYLD_FALLBACK_LIBRARY_PATH')


user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil.dbConnect("'mode'", user, password)

unique_steps = dbUtil.getUniqueSteps(cur, conn)

start = unique_steps[0][1]
end = unique_steps[0][3]

linkList = []
counter = 0

start_time = time.time()

print('Mapping: ', len(unique_steps), 'Unique routes')
sys.stdout.write("\r%d%%" % ((counter/len(unique_steps)*100)))
for index, step in enumerate(unique_steps):
    if index > 3:
        break
    elapsed_time = time.time() - start_time

    if elapsed_time >= 1:
        sys.stdout.write("\r%d%%" % ((counter/len(unique_steps)*100)))
        sys.stdout.flush()

    step_id = step[0]
    start_node = step[1]
    end_node = step[3]

    links = dbUtil.getLinksInStep(cur, conn, start_node, end_node)

    for link in links:
        if(link[1] != -1):
            linkList.append((step_id, link[0], link[1]))

    counter = counter + 1

#dbUtil.deleteStepLinks(cur,conn)
#dbUtil.storeStepLinks(cur, conn, linkList)

print('Creating route step links')
dbUtil.createRouteStepLinks(cur, conn)
print('Route Mapping complete')
