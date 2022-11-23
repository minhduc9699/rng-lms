import pymysql.cursors

def get_connection():
    return pymysql.connect(host='14.225.16.22',
        port=3360,
        user='root',
        password='strongAsF@ck',
        database='CenterDatabases',
        cursorclass=pymysql.cursors.DictCursor)
