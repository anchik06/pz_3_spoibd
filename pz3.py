import mysql.connector

cnx = mysql.connector.connect(
    host="srv221-h-st.jino.ru",
    database="j30084097_137",
    user="j30084097_137",
    password="Gruppa137")


cur = cnx.cursor()

cur.execute("SELECT CURDATE()")

row = cur.fetchone()
print("Current date is: {0}".format(row[0]))

cnx.close()
