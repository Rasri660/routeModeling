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

        if i[3] != i[6]:
            prev_step = data[index + 1][0]
            current_step = data[index][0]
            prev_end_node = data[index + 1][8]
            current_start_node = data[index][4]
            sequence_number = data[index + 1][2]
            if current_start_node != prev_end_node:
            #print(current_step, prev_step, current_start_node, prev_end_node, sequence_number)
                print('update:', prev_step, sequence_number)
                dbUtil_routeFixer.updateStep(cur, conn, prev_step, sequence_number)
