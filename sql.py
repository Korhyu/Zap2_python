import MySQLdb

db = MySQLdb.connect(host="localhost",   # your host, usually localhost
                     user="zap2app",        # your username
                     passwd="zap2app",      # your password
                     db="zap2")             # name of the data base

# you must create a Cursor object. It will let
# you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM prueba")

# print all the first cell of all the rows
for row in cur.fetchall():
    print (row[0], row[1], row[2], row[3])

db.close()