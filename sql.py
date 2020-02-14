import MySQLdb

db = MySQLdb.connect(host="10.10.10.115",   # your host, usually localhost
                     user="zap2app",        # your username
                     passwd="zap2app",      # your password
                     db="zap2")             # name of the data base
'''
db = MySQLdb.connect(host="localhost",
                     user="zap2app",
                     passwd="zap2app",
                     db="zap2")
'''

# you must create a Cursor object. It will let
# you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM prueba")

# print all the first cell of all the rows
for row in cur.fetchall():
    print (row[0], row[1], row[2], row[3])

db.close()