import sqlite3 as lite
import sys
from vardata import *

con = lite.connect(dbname)

with con:
	cur = con.cursor()
	cur.execute("DELETE FROM Comments")
	cur.execute("UPDATE Players SET Stock = 0")
