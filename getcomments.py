import praw

Player_Okafor = ('okafor','okafor')
Player_Towns = ('towns','towns')
Player_Winslow = ('winslow','winslow')
Player_Mudiay = ('Mudiay', 'mudiay')
Player_Russell = ("D'Angelo",'russell')
Player_Porzingis = ('Porzingis','porzingis')
Player_WCS = ('Willie','wcs')
Player_Hezonja = ('Hezonja','hezonja')
Player_Stanley = ('Stanley Johnson','johnson')


player = Player_Mudiay
#What player are we searching for?

r = praw.Reddit('Comment Scraper for DraftStocked')
subreddit = r.get_subreddit('nba')
submissions = subreddit.search(player[0], sort='relevance',period='month')

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
			comment_list.append((comment.score,comment.body,comment.permalink))


print("AGGREGATED COMMENTS: ")

comment_list.sort(key=lambda x: x[0], reverse=True)

for sc,bd,pm in comment_list:
	print(pm)
	print(bd+'\n')


