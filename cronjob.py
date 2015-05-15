
#Cronjob script to update our database file
import sqlite3 as lite
import sys
from vardata import *
from getcomments import *
import time

con = lite.connect(dbname)
currentTime = int(time.time())


for player in PlayerList:
	sem = 0
	with con:
		cur = con.cursor()
		cur.execute("SELECT Semantic,Dateposted FROM Comments WHERE player = ?",(player.nickname,))
		rows = cur.fetchall()
		for row in rows:
			if (currentTime - row[1] > secondsMonth):
				sem += row[0]
		cur.execute("UPDATE Players SET Stock=Stock-? WHERE Fullname=?",(sem,player.nickname))
		cur.execute("DELETE FROM Comments WHERE (?-Dateposted) > ? AND player=?",(currentTime,secondsMonth,player.nickname))
	ParseComments(player,day)
	#Update with new comments and values


print ("Script ran on: "+time.strftime("%I:%M:%S"))