import pymysql.cursors

connection = pymysql.connect(host='localhost',
    user='user',
    password='passwd',
    database='db',
    cursorclass=pymysql.cursors.DictCursor)