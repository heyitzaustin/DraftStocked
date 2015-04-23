import sqlite3 as lite
import sys

con = lite.connect('redditdata.db')

with con:
	cur = con.cursor()
	cur.execute("DELETE FROM Comments")
	cur.execute("UPDATE Players SET Stock = 0")