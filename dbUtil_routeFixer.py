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

def getUniqueRoutes(cur, conn):
    route_list = None
    if cur != None:
        try:
            cur.execute("""SELECT route_id, id
                            FROM
                            (
                            	SELECT ROW_NUMBER() OVER(PARTITION BY id) as rw, route_id, id
                            	FROM vm.vm_routes
                            ) AS q1
                            WHERE rw = 1""")

        except:
            print('I cant SELECT from database')

        route_list = cur.fetchall()
        return route_list

    else:
        print('No db connection established, try running dbConnect() first')
        return None


def getRouteStepLinks(cur, conn, route_id):
    print(route_id)
    if cur != None:
        try:
            cur.execute("""WITH test AS (SELECT *
                                        	FROM
                                        	(
                                        		SELECT route_id, route_step_links.step_id, step_index, sequence_number
                                        		FROM vm.route_step_links
                                        		INNER JOIN vm.step_links
                                        		ON step_links.step_id = route_step_links.step_id
                                        		WHERE route_id = '1077:1:1'
                                        		ORDER BY step_index, sequence_number
                                        	) AS q1
                                        )

                                        SELECT q5.step_id, step_index, max,start_link, start_link_start_node, start_link_end_node, end_link, from_ref_nodeid AS end_link_start_node, to_ref_nodeid AS end_link_end_node
                                        --SELECT *
                                        FROM
                                        (
                                        	SELECT q4.step_id, step_index, max,start_link, from_ref_nodeid AS start_link_start_node, to_ref_nodeid AS start_link_end_node, end_link
                                        	FROM
                                        	(
                                        	SELECT q3.step_id, step_index, max, ref_lid_link as start_link ,end_link
                                        		FROM
                                        		(
                                        			SELECT q2.step_id, step_index, max, ref_lid_link as end_link
                                        			FROM
                                        			(
                                        				SELECT step_index, step_id, max(sequence_number)
                                        				FROM test
                                        				GROUP BY step_id, step_index
                                        				ORDER BY step_index
                                        			) AS q2

                                        			INNER JOIN vm.step_links
                                        			ON q2.step_id = step_links.step_id AND step_links.sequence_number = q2.max
                                        			ORDER BY step_index
                                        		)AS q3
                                        		INNER JOIN vm.step_links
                                        		ON step_links.step_id = q3.step_id
                                        		WHERE step_links.sequence_number = 0
                                        		ORDER BY step_index
                                        	) AS q4
                                        	INNER JOIN vm.ref_link_parts_network
                                        	ON start_link = ref_link_parts_network.ref_lid
                                        ) AS q5

                                        INNER JOIN vm.ref_link_parts_network
                                        ON end_link = ref_link_parts_network.ref_lid
                                        ORDER BY step_index DESC""")
        except:
            print('I cant SELECT from database')

        closest_source = cur.fetchall()
        return closest_source

def updateStep(cur, conn, step_id, sequence_number):
    if cur != None:
        try:
            cur.execute("""UPDATE vm.step_links
                            SET link_usage = false
                            WHERE step_id = %s AND sequence_number = %s""", [step_id, sequence_number])
            conn.commit()
        except:
            print('I cant SELECT from database')


    else:
        print('No db connection established, try running dbConnect() first')
        return None
