import mysql.connector

cnx = mysql.connector.connect(
    host="",
    database="",
    user="",
    password="")


cur = cnx.cursor()

cur.execute("SELECT CURDATE()")

row = cur.fetchone()
print("Current date is: {0}".format(row[0]))

cnx.close()

