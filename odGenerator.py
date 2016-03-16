#odGeneraotr.py

import psycopg2 #run export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib:$DYLD_FALLBACK_LIBRARY_PATH
import dbUtil

#Connect to DB
user = input('User: ')
password = input('Password: ')

user = "'" + user + "'"
password = "'" + password + "'"

[cur, conn] = dbUtil.dbConnect("'mode'", user, password)

print(cur, conn)

try:
	cur.execute("""SELECT DISTINCT(vmid) FROM vm.vmid_samsid_key""")
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

#write OdPairs To Database
try:
	cur.execute("""DELETE FROM vm.vm_od_max""")
	conn.commit()
except:
    print ("Did not insert to database")

try:
	cur.executemany("""INSERT INTO vm.vm_od_max (od_id,vm_oid,vm_did,white_list) VALUES(%s,%s,%s,true)""", odPairs)
	conn.commit()
except:
    print ("Did not insert to database")

print('Script complete')
