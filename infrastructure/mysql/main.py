import pymysql.cursors

def get_connection():
    return pymysql.connect(host='',
        port=3360,
        user='root',
        password='',
        database='CenterDatabases',
        cursorclass=pymysql.cursors.DictCursor)
