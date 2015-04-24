
#Cronjob script to update our database file
import sqlite3 as lite
import sys
from vardata import *

con = lite.connect(dbname)

with con:
	cur = con.cursor()
	cur.execute("DELETE FROM Comments")
	cur.execute("UPDATE Players SET Stock = 0")
	#Reset our table

for player in PlayerList:
	ParseComments(player)
	#Update with new comments and values