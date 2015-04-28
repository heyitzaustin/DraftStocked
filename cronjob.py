
#Cronjob script to update our database file
import sqlite3 as lite
import sys
from vardata import *
from getcomments import *
import time

con = lite.connect(dbname)

with con:
	cur = con.cursor()
	cur.execute("DELETE FROM Comments")
	#Reset our table

for player in PlayerList:
	ParseComments(player)
	#Update with new comments and values

print ("Script ran on: "+time.strftime("%I:%M:%S"))