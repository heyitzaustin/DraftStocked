import praw
import requests
import json
import datetime
import time
from vardata import *


player = Player_Russell
#What player are we searching for?
timeFrame = month
#How far back are we looking?

r = praw.Reddit('Comment Scraper for DraftStocked')
multi_reddits = r.get_subreddit('nba+NBA_Draft')
submissions = multi_reddits.search(player[0], sort='relevance',period=timeFrame)

comment_list = []
for x in submissions:
	print(str(x))
	print(x.id)
	submission = r.get_submission(submission_id=x.id)
	submission.replace_more_comments(limit=16, threshold=10)
	flat_comments = praw.helpers.flatten_tree(submission.comments)
	for comment in flat_comments:
		if player[1] in (comment.body).lower() and comment.id not in comment_list:
			#print(comment.body)
			#print('\n')
			#Debug stuff
			comment_list.append((comment.score,comment.body,comment.permalink,comment.created_utc))


print("\nAGGREGATED COMMENTS:\n")

comment_list.sort(key=lambda x: x[0], reverse=True)

playerStock = 0
#Initialize player stock

displayAmount = 25
#How many comments to display?
timeFilter = secondsMonth
#View comments from the past ____ 

currentTime = int(time.time())
#tuple is of comment score, comment body, comment permalink, comment date posted
for sc,bd,pm,dt in comment_list:
	#Post request to semantic analysis API. This is how we're determining whether a 
	#comment is helping or detrimental to the players stock.
	response = requests.post("https://twinword-sentiment-analysis.p.mashape.com/analyze/",
  	headers={
    "X-Mashape-Key": "V1YkqJPoHwmshbjpJICAEF9E2ublp1W2P3qjsnfbuwdxTHdUTj",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
  	},
  	params={
    "text": bd
  	}
	)
	playerStock+=response.json()["score"]
	#print(response.json())

	if(displayAmount>=0):
		if(currentTime-dt < timeFilter and sc > 0):
			print("COMMENT #"+str(25-displayAmount))
			print('Context: '+pm)
			print('Comment Score: '+str(sc))
			print("Date Posted:"+datetime.datetime.fromtimestamp(int(dt)).strftime('%Y-%m-%d %H:%M:%S'))
			print(bd+'\n')
			displayAmount+= -1
	else:
		print('.', end="", flush=True)

print("\nPlayer stock of "+player[2]+" is %.2f" % round(playerStock,2))


