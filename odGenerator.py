#odGeneraotr.py

import psycopg2

try:
    conn = psycopg2.connect("dbname='mode' user='mms' host='localhost' password='001'")
except:
    print ("I am unable to connect to the database")

cur = conn.cursor()

try:
	cur.execute("""SELECT vmid FROM vm.vm_zones ORDER BY vmid""")
except:
    print('I cant SELECT from database')

vmidList = cur.fetchall()

nmbrRows = len(vmidList)
odPairs = []
i = 0

while(i < nmbrRows):
    j = 0
    while(j < nmbrRows):
        a = [len(odPairs)+1,vmidList[i][0], vmidList[j][0]]
        odPairs.append(a)
        j = j + 1
    i = i + 1

print(odPairs)

#writeOdPairsToDatabase
try:
	cur.execute("""DELETE FROM vm.vm_od_max""")
	conn.commit()
except:
    print ("Did not insert to database")

try:
	cur.executemany("""INSERT INTO vm.vm_od_max (od_id,vm_oid,vm_did) VALUES(%s,%s,%s)""", odPairs)
	conn.commit()
except:
    print ("Did not insert to database")
