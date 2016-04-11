import psycopg2



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
                            WHERE white_list = true""")
                            #WHERE (vm_oid BETWEEN 20 AND 25) AND (vm_did BETWEEN 20 AND 25)""")
                            #WHERE (vm_oid >= 8 AND vm_did >= 10)""")
                            #WHERE (vm_oid BETWEEN 20 AND 30) AND (vm_did BETWEEN 9 AND 30)
                            #WHERE white_list = true
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
        	cur.execute("""TRUNCATE vm.vm_google_routes_raw RESTART IDENTITY""")
        	conn.commit()
        except:
            print('Could not delete from DB')
    else:
        print('Not db connection established, try running dbConnect() first')

#QUERY to delete previous routes
def storeRoutes(cur, conn, r):
    if cur != None:
        try:
        	cur.executemany("""INSERT INTO vm.vm_google_routes_raw_nk (od_id, route_id, start_point, end_point, route_index, step_index, travel_time, distance, time_period, start_time, date_inserted) VALUES (%(od_id)s, %(route_id)s, %(start_point)s, %(end_point)s, %(route_index)s, %(step_index)s, %(travel_time)s, %(distance)s, %(time_period)s, %(start_time)s, %(date_inserted)s)""", r)
        	conn.commit()
        except:
            print ("Can't write to database...")
    else:
        print('Not db connection established, try running dbConnect() first')

def getDistinctSteps(cur, conn):
    distinct_routes = None
    if cur != None:
        try:
            cur.execute("""SELECT DISTINCT start_point, end_point FROM vm.vm_google_routes_raw""")
        except:
            print('I cant SELECT from database')

        distinct_routes = cur.fetchall()
        return distinct_routes

    else:
        print('No db connection established, try running dbConnect() first')
        return None


def getClosestSource(cur, conn, start):
    closest_source = None
    if cur != None:
        try:
            cur.execute("SELECT * FROM(SELECT from_ref_nodeid, ST_DISTANCE(ST_STARTPOINT(vm.ref_link_parts_network.geom), ST_TRANSFORM(ST_GeomFromText(ST_AsEWKT( %s ), 4326), 3006)) FROM vm.ref_link_parts_network WHERE vm.ref_link_parts_network.functional_road_class <=6 ORDER BY st_distance ASC LIMIT 1) AS FIRST", [start])
        except:
            print('I cant SELECT from database')

        closest_source = cur.fetchall()
        return closest_source

    else:
        print('No db connection established, try running dbConnect() first')
        return None

def getClosestTarget(cur, conn, end):
    closest_Target = None
    if cur != None:
        try:
            cur.execute("SELECT * FROM(SELECT to_ref_nodeid, ST_DISTANCE(ST_ENDPOINT(vm.ref_link_parts_network.geom), ST_TRANSFORM(ST_GeomFromText(ST_AsEWKT( %s ), 4326), 3006)) FROM vm.ref_link_parts_network WHERE vm.ref_link_parts_network.functional_road_class <= 6 ORDER BY st_distance ASC LIMIT 1) AS FIRST", [end])
        except:
            print('I cant SELECT from database')
        closest_Target = cur.fetchall()

        return closest_Target

    else:
        print('No db connection established, try running dbConnect() first')
        return None


def getLinksInStep(cur, conn, start_node, end_node):

    start_node = start_node[0][0]
    end_node = end_node[0][0]

    links = None
    if cur != None:
        try:
            cur.execute("SELECT seq, id2 AS edge, cost FROM pgr_dijkstra('SELECT vm.ref_link_parts_network.ref_lid AS id, CAST(vm.ref_link_parts_network.from_ref_nodeid AS int) AS source,  CAST(vm.ref_link_parts_network.to_ref_nodeid AS int) AS target, vm.ref_link_parts_network.cost AS cost FROM vm.ref_link_parts_network WHERE vm.ref_link_parts_network.functional_road_class <= 6', %s, %s, false, false) ORDER BY seq ASC", [start_node, end_node])
        except:
            print('I cant SELECT from database')

        links = cur.fetchall()
        return links

    else:
        print('No db connection established, try running dbConnect() first')
        return None

def storeUniqueSteps(cur, conn, dataToStore):
    if cur != None:
        try:
        	cur.executemany("""INSERT INTO vm.unique_steps (step_id, start_node, end_node, start_point, end_point) VALUES (%s, %s, %s, %s)""", dataToStore)
        	conn.commit()
        except:
            print ("Can't write to database...")
    else:
        print('Not db connection established, try running dbConnect() first')
