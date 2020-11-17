from database.db_connection import pymysql, connectionHandler

# Generic function for handeling queries to the database
# Returns results
def doQuery(query, parameters = None) :
    try :
        with connectionHandler.getConnection().cursor() as cursor:
            cursor.execute(query, parameters)
            print('Last query executed succesfully: {}'.format(cursor._last_executed))
            connectionHandler.closeConnection()
            return cursor.fetchall()
    except pymysql.Error as e :
        print("Error occured while executing a query: {}".format(e))
        connectionHandler.closeConnection()
        return None