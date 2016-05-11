import dbUtil_routeFixer
import time
import sys



user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil_routeFixer.dbConnect("'mode'", user, password)

distinct_routes = dbUtil_routeFixer.getUniqueRoutes(cur, conn)

number_routes = len(distinct_routes)
#print(number_routes)

start_index = #Define star
end_index = #Define end

route_range = range(start_index, end_index)
start_time = time.time()
sys.stdout.write("\r%d%%" % ((0/end_index*100)))

for outer_index, route in enumerate(route_range):
    sys.stdout.write("\r%d%%" % (((outer_index)/(end_index - start_index)*100)))
    route_id = distinct_routes[route][0]
    #print(route_id)
    data = dbUtil_routeFixer.getRouteStepLinks(cur, conn, route_id)
    #print(data)
    #data = dbUtil_routeFixer.getRouteStepLinks(cur, conn, '1077:1:1')
    number_steps = len(data)
    for index, i in enumerate(data):
        if index + 1 < number_steps:

            prev_step = data[index + 1][0]
            current_step = data[index][0]
            prev_end_link_end_node = data[index + 1][8]
            prev_end_link_start_node = data[index + 1][7]
            current_start_link_start_node = data[index][4]
            prev_sequence_number = data[index + 1][2]
            current_sequence_number = data[index][2]
            update = 'false'

            if current_start_link_start_node != prev_end_link_end_node:
                if current_start_link_start_node == prev_end_link_start_node:
                    update = 'true'
                    #print('update:', prev_step, prev_sequence_number, update)
                    dbUtil_routeFixer.updateStep(cur, conn, prev_step, prev_sequence_number)
