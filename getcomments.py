import praw
import requests
import json
import datetime
import time
import sqlite3 as lite
import sys

from vardata import *

debug = 0;
#Set to 1 for print statements

con = lite.connect(dbname)

def ParseComments(player,timeFrame):

	#How far back are we looking?

	r = praw.Reddit('Comment Scraper for DraftStocked by u/heyitzaustin')
	multi_reddits = r.get_subreddit('nba+NBA_Draft')
	#looking at these two subreddits for now so we're sure to get relevant content
	searchterm = player.search
	submissions = multi_reddits.search(searchterm, sort='relevance',period=timeFrame)
	#getting the submissions!
	
	if debug:
		print("\nDraft Stock report on "+player.fullname+"\n")
	comment_list = []
	
	for x in submissions:
		if debug:
			print(str(x))
			print(x.id)
			#Debug stuff
		submission = r.get_submission(submission_id=x.id)
		submission.replace_more_comments(limit=0, threshold=0)
		# ^ we don't really care about lower level/reply comments. Set limit to 0 so fewer API calls
		flat_comments = praw.helpers.flatten_tree(submission.comments)
		for comment in flat_comments:
			if player.nickname in (comment.body).lower() and comment.id not in comment_list:
				comment_list.append(Comment(comment.score,comment.body,comment.permalink,comment.created_utc))
				#if the player was mentioned in the comment, create a comment object and add to our list
		


	#We got the comments! Now let's sort them
	if debug:
		print("\nAGGREGATED COMMENTS:\n")

	comment_list.sort(key=lambda x: x.score, reverse=True)
	#sorting my score/Karma
	#playerStock = 0
	playerStock = 0
	#Initialize player stock
	displayAmount = 25
	#How many comments to display?
	timeFilter = secondsMonth
	#View comments from the past ____ 
	currentTime = int(time.time())
	#Current time for comparison

	#tuple is of comment score, comment body, comment permalink, comment date posted
	for comment in comment_list:
		#Post request to semantic analysis API. This is how we're determining whether a 
		#comment is helping or detrimental to the players stock.
		response = requests.post("https://twinword-sentiment-analysis.p.mashape.com/analyze/",
  		headers={
    	"X-Mashape-Key": "V1YkqJPoHwmshbjpJICAEF9E2ublp1W2P3qjsnfbuwdxTHdUTj",
    	"Content-Type": "application/x-www-form-urlencoded",
    	"Accept": "application/json"
  		},
  		params={
    	"text": comment.body
  		}
		)
		playerStock+=response.json()["score"]
		#increment the player's stock by the semantic analysis score
		
		#Just debug stuff. For terminal use so it doesn't get overcrowded
		if debug:
			if(displayAmount>=0):
				if(currentTime-comment.date_posted < timeFilter and comment.score > 0):
					print("COMMENT #"+str(25-displayAmount))
					print('Context: '+comment.permalink)
					print('Comment Score: '+str(comment.score))
					print("Date Posted:"+datetime.datetime.fromtimestamp(int(comment.date_posted)).strftime('%Y-%m-%d %H:%M:%S'))
					print(comment.body+'\n')
					displayAmount+= -1
			else:
				print('.', end="", flush=True)
				#Let's us know the script is still running

		with con:
			params = (player.nickname,comment.score, comment.body, comment.permalink, comment.date_posted,response.json()["score"])
			cur = con.cursor()
			cur.execute("INSERT INTO Comments VALUES(?,?,?,?,?,?)",params)
			#Add to our local SQL database!

	with con:
		cur = con.cursor()
		cur.execute("SELECT Stock,Change FROM Players WHERE Fullname=?",(player.fullname,))
		row = cur.fetchone()
		#cur.execute("UPDATE Players SET Change =? WHERE Fullname =?",(round( playerStock, 2 ), player.fullname))
		cur.execute("UPDATE Players SET Change =? WHERE Fullname =?",(round(row[1]+ playerStock, 2 ), player.fullname))
		#Get difference in stocks to measure change
		#cur.execute("UPDATE Players SET Stock=? WHERE Fullname=?", (round(row[0]+playerStock,2), player.fullname))
		cur.execute("UPDATE Players SET Stock=? WHERE Fullname=?", (round(row[0] + playerStock,2), player.fullname))
		#update our player info to have new stock
		
	print("\nPlayer stock of "+player.fullname+" is %.2f" % round(row[0] + playerStock,2))


def getComments(player):
	with con:

		cur = con.cursor()
		cur.execute("SELECT Score,Body,Permalink,Dateposted FROM Comments WHERE Player=?",(player.nickname,))
		rows = cur.fetchall()

		for row in rows:
			print("Context: "+row[2])
			print("Score: "+str(row[0]))
			t = datetime.datetime.fromtimestamp(row[3]).strftime('%m-%d-%Y')
			print("Posted: "+t)
			print(row[1]+"\n")
