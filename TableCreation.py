import sqlite3 as lite
import sys
from vardata import *

con = lite.connect(dbname)

with con:
	cur = con.cursor()
	cur.execute("CREATE TABLE Players(Search TEXT, Nickname TEXT, Fullname TEXT, Stock INT)")
	cur.execute("CREATE TABLE Comments(Player TEXT, Score INT, Body TEXT, Permalink TEXT, Dateposted INT)")


	#Insert into database what players you want to know about!
	#Variables are tuples of 3: (A,B,C) where:
	#A = reddit search term. something distinguishable
	#B = nickname or shorthand, what he is usually called
	#C = Full name 
	for player in PlayerList:
		params = (player.search,player.nickname,player.fullname)
		cur.execute("INSERT INTO Players VALUES(?,?,?,0)",params)


