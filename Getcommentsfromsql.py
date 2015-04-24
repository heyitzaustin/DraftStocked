import sqlite3 as lite
import sys
from vardata import *

con = lite.connect(dbname)

with con:

	cur = con.cursor()
	cur.execute("SELECT * FROM Comments")

	rows = cur.fetchall()

	for row in rows:
		print(row)
		print('\n')
