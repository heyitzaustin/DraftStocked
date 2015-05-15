# DraftStocked

http://192.241.216.121/

List of important files in this repository:

getcomments.py:

The bulk of our data aggregation, parsing, storing, and analysis. This file contains the vital 'ParseComments' function which combs through reddit for important comments before storing it into our SQL database

vardata.py:

File with object declarations as well as important values that allow the script to function.

cronjob.py:

Our script that we have running on our VPS which daily updates our database

Getcommentsfromsql.py:
Getplayersfromsql.py:
TableCreation.py:
ResetTables.py:
updateall.py:

Testing scripts for our SQL database. Not too important in the scope of our program
