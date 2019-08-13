import pymysql
import sys

# PASSWD = open('passwd.txt').read()

class MySQL(object):
    '''
    MySQL
    '''
    conn = ''
    cursor = ''
 
    def __init__(self, host='localhost', user='root', passwd='528012', db='data_load'):
 
        """MySQL Database initialization """
        try:
            self.conn = pymysql.connect(host, user, passwd, db,charset="utf8")
        except Exception:
            sys.exit()
 
        self.cursor = self.conn.cursor()
 
    def query(self, sql):
        """  Execute SQL statement """
        return self.cursor.execute(sql)
 
    def commit(self):
        """ Return the results after executing SQL statement """
        return self.conn.commit()
 
    def show(self):
        """ Return the results after executing SQL statement """
        return self.cursor.fetchall()
 
    # def __del__(self):
    #     """ Terminate the connection """
    #     self.conn.close()
    #     self.cursor.close()


