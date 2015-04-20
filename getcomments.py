import praw

r = praw.Reddit('Comment Scraper for DraftStocked')
#r.login('Draftstocked','shonen')
subreddit = r.get_subreddit('nba')
submissions = subreddit.search('okafor', sort='top',period='month')

comment_list = []
for x in submissions:
	print(str(x))
	print(x.id)
	submission = r.get_submission(submission_id=x.id)
	submission.replace_more_comments(limit=16, threshold=10)
	flat_comments = praw.helpers.flatten_tree(submission.comments)
	for comment in flat_comments:
		if " he " in comment.body and comment.id not in comment_list:
			print('COMMENT:')
			print(str(comment))
			comment_list.append((comment.score,comment.body))


print("AGGREGATED COMMENTS: ")

comment_list.sort(key=lambda x: x[0], reverse=True)

for sc,bd in comment_list:
	print(sc)
	print(bd)


