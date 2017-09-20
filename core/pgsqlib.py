import psycopg2
dbhost = ''
dbuser = 'mia'
dbpass = ''
dbname = 'db_routing_sdn'
dbport = 5432

conn = psycopg2.connect(host = dbhost,
               user = dbuser,
                password = dbpass,
                database = dbname,
                port = dbport)

def fetch(sql):

    cursor = conn.cursor()
    rs = None

    try:
        cursor.execute(sql)
        rs = cursor.fetchall()

    except psycopg2.Error as e:
        print(e.pgerror)
        rs = 'error'
        # logging("%s: Data Not Found" % (botName), folder_debug, MYMOD)
        #print "data not found"
    cursor.close()
    return rs

def execScalar(sql):
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        conn.commit()
        rowsaffected = cursor.rowcount

    except psycopg2.Error as e:
        print(e.pgerror)
        rowsaffected = -1
        conn.rollback()
        # logging("%s: Error Exec SQL" % (botName), folder_debug, MYMOD)
        #print "error bro"
    cursor.close()
    return rowsaffected