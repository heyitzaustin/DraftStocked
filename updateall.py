from vardata import *
from getcomments import *

print("Starting Update of Database!")

for player in PlayerList:
	GetComments(player)