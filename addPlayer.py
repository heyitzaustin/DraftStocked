import sqlite3 as lite
import sys
from vardata import *
from getcomments import *

con = lite.connect(dbname)

def addPlayer(player):
	with con:
		cur=con.cursor()
		params = (player.search,player.nickname,player.fullname)
		cur.execute("INSERT INTO Players VALUES(?,?,?,0,0)",params)
	ParseComments(player,month)