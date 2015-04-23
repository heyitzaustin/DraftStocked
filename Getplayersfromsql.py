import sqlite3 as lite
import sys

con = lite.connect('redditdata.db')

with con:

	cur = con.cursor()
	cur.execute("SELECT * FROM Players")

	rows = cur.fetchall()

	for row in rows:
		print(row)
