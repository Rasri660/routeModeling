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

rows = cur.fetchall()
nmbrRows = len(rows)
test = []
i = 0
while(i < nmbrRows):
    j = 0
    while(j < nmbrRows):
        a = [rows[i][0], rows[j][0]]
        test.append(a)
        j = j + 1;
    i = i + 1

print(test)
