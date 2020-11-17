import pymysql

class ConnectionHandler() : 
    connectionInstance = None

    def createConnection(self) :
        self.connectionInstance = pymysql.connect(host='localhost',
                                user='root',
                                password='root',
                                db='mydb',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor,
                                autocommit=True)

    def getConnection(self) :
        if self.connectionInstance is None :
            self.createConnection()
        
        return self.connectionInstance

    def closeConnection(self) :
        if self.connectionInstance is not None :
            self.connectionInstance.close()

        self.connectionInstance = None

connectionHandler = ConnectionHandler()