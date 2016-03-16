import psycopg2 #run export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib:$DYLD_FALLBACK_LIBRARY_PATH


#Initialise connection to DB
def dbConnect(name, usr, pas):

    try:
        conn = psycopg2.connect("dbname=" + name + "user=" + usr + "host='localhost' password=" + pas + "")
        print('Connection to db established')
    except:
        print ("I am unable to connect to the database")

    cur = conn.cursor()
    return [cur, conn]


#QUERY to extract all OD-relations where routes shall be extracted from google.
def getOdList( cur ):
    vmidList = None
    if cur != None:
        try:
            cur.execute("""SELECT od_id, vm_oid, vm_did
                            FROM vm.vm_od_max
                            WHERE (vm_oid = 8 AND vm_did = 22)""")
        except:
            print('I cant SELECT from database')

        vmid_list = cur.fetchall()
        return vmid_list

    else:
        print('No db connection established, try running dbConnect() first')
        return None

#Query to get start and end points for all vm_zones
def getNodeList(cur):
    node_list = None
    if cur != None:
        try:
    	       cur.execute("""SELECT vmid,ST_Y(ST_TRANSFORM(node_geom,4326)),ST_X(ST_TRANSFORM(node_geom,4326))
                            FROM vm.vm_zones
                            ORDER BY vmid """)
        except:
            print('I cant SELECT from database')

        node_list = cur.fetchall()

        return node_list
    else:
        print('Not db connection established, try running dbConnect() first')
        return None

#QUERY to get time periods
def getTimePeriods(cur):
    time = None
    if cur != None:
        try:
        	cur.execute("""SELECT *
                            FROM vm.vm_time_period""")
        except:
            print('I cant SELECT from database')

        time_periods = cur.fetchall()
        return time_periods

    else:
        print('Not db connection established, try running dbConnect() first')
        return None

#QUERY to delete previous routes
def deleteRoutes(cur, conn):
    if cur != None:
        try:
        	cur.execute("""DELETE FROM vm.vm_google_routes_raw""")
        	conn.commit()
        except:
            print('Could not delete from DB')
    else:
        print('Not db connection established, try running dbConnect() first')

#QUERY to delete previous routes
def storeRoutes(cur, conn, r):
    if cur != None:
        try:
        	cur.executemany("""INSERT INTO vm.vm_google_routes_raw (od_id, route_id, start_point, end_point, route_index, step_index, travel_time, distance, time_period, start_time, date_inserted) VALUES (%(od_id)s, %(route_id)s, %(start_point)s, %(end_point)s, %(route_index)s, %(step_index)s, %(travel_time)s, %(distance)s, %(time_period)s, %(start_time)s, %(date_inserted)s)""", r)
        	conn.commit()
        except:
            print ("Can't write to database...")
    else:
        print('Not db connection established, try running dbConnect() first')
