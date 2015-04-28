#Player object
class Player:
	def __init__(self,search,nickname,fullname):
		self.search = search
		self.nickname = nickname
		self.fullname = fullname

#Comment object
class Comment:
	def __init__(self,score,body,permalink,date_posted):
		self.score = score
		self.body = body
		self.permalink = permalink
		self.date_posted = date_posted


dbname = '/root/DraftStocked/redditdata.db'
#dbname = 'redditdata.db'

#Player Database
Okafor = Player('okafor','okafor','Jahlil Okafor')
Towns = Player('towns','towns','Karl Anthony-Towns')
Winslow = Player('winslow','winslow','Justice Winslow')
Mudiay = Player('Mudiay', 'mudiay', 'Emmanuel Mudiay')
Russell = Player("D'Angelo",'russell',"D'Angelo Russell")
Porzingis = Player('Porzingis','porzingis','Kristaps Porzingis')
WCS = Player('Willie','wcs','Willie Cauley-Stein')
Hezonja = Player('Hezonja','hezonja','Mario Hezonja')
Stanley = Player('Stanley Johnson','johnson','Stanley Johnson')
#Variables are tuples of 3: (A,B,C) where:
#A = reddit search term. something distinguishable
#B = nickname or shorthand, what he is usually called
#C = Full name 

PlayerList = [Okafor,Towns,Winslow,Mudiay,Russell,Porzingis,WCS,Hezonja,Stanley]

#Time parameters for API
year = 'year'
month = 'month'
week = 'week'
day = 'day'

#for filtering comments (UNIX timestamp subtraction)
secondsYear = 31536000
secondsMonth = 2678400 
secondsWeek = 604800
secondsDay = 86400
