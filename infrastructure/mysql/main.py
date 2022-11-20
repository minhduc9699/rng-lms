import pymysql.cursors

def get_connection():
    return pymysql.connect(host='localhost',
        user='user',
        password='passwd',
        database='db',
        cursorclass=pymysql.cursors.DictCursor)