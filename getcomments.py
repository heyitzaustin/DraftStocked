import praw
import requests
import json
import datetime
import time
import sqlite3 as lite
import sys

from vardata import *

con = lite.connect('redditdata.db')

def ParseComments(player):

	timeFrame = month
	#How far back are we looking?

	r = praw.Reddit('Comment Scraper for DraftStocked')
	multi_reddits = r.get_subreddit('nba+NBA_Draft')

	submissions = multi_reddits.search(player.search, sort='relevance',period=timeFrame)

	print("\nDraft Stock report on "+player.fullname+"\n")
	comment_list = []
	for x in submissions:
		print(str(x))
		print(x.id)
		submission = r.get_submission(submission_id=x.id)
		submission.replace_more_comments(limit=0, threshold=0)
		# ^ This is our bottleneck. See if we can make it faster?
		flat_comments = praw.helpers.flatten_tree(submission.comments)
		for comment in flat_comments:
			if player.nickname in (comment.body).lower() and comment.id not in comment_list:
				#print(comment.body)
				#print('\n')
				#Debug stuff
				comment_list.append(Comment(comment.score,comment.body,comment.permalink,comment.created_utc))
		


	print("\nAGGREGATED COMMENTS:\n")

	comment_list.sort(key=lambda x: x.score, reverse=True)

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
		#print(response.json())

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

		with con:
			params = (player.fullname,comment.score, comment.body, comment.permalink, comment.date_posted)
			cur = con.cursor()
			cur.execute("INSERT INTO Comments VALUES(?,?,?,?,?)",params)

	with con:
		cur = con.cursor()
		cur.execute("UPDATE Players SET Stock=? WHERE Fullname=?", (round(playerStock,2), player.fullname)) 
	print("\nPlayer stock of "+player.fullname+" is %.2f" % round(playerStock,2))

def getComments(player):
	with con:

		cur = con.cursor()
		cur.execute("SELECT Score,Body,Permalink,Dateposted FROM Comments WHERE Player=?",(player.fullname,))
		rows = cur.fetchall()

		for row in rows:
			print("Context: "+row[2])
			print("Score: "+str(row[0]))
			print("Posted: "+str(row[3]))
			print(row[1]+"\n")
