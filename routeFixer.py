import dbUtil_routeFixer

user = 'vm-user'
password = '001'

user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil_routeFixer.dbConnect("'mode'", user, password)

#distinct_routes = dbUtil_routeFixer.getUniqueRoutes(cur, conn)

data = dbUtil_routeFixer.getRouteStepLinks(cur, conn, '1077:1:1')
number_steps = len(data)
print(number_steps)
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
                print('update:', prev_step, prev_sequence_number, update)
                dbUtil_routeFixer.updateStep(cur, conn, prev_step, prev_sequence_number)
            #print(current_step, prev_step, current_start_node, prev_end_node, sequence_number)

                #dbUtil_routeFixer.updateStep(cur, conn, prev_step, sequence_number)
