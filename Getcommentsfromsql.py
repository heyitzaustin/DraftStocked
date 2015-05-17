import sqlite3 as lite
import sys
from vardata import *
import datetime

con = lite.connect(dbname)

with con:

	cur = con.cursor()
	cur.execute("SELECT * FROM Comments")

	rows = cur.fetchall()

	for row in rows:
		print("Comment about: "+row[0])
		print("Score: "+str(row[1]))
		t = datetime.datetime.fromtimestamp(row[4]).strftime('%m-%d-%Y')
		print("Date Posted: "+t)
		print("semantic score: "+str(row[5]))
		print(row[2])

		print('\n')
