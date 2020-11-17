import pymysql

# Class for handeling connections to the database

class ConnectionHandler() : 
    def __init__(self) :
        self.connectionInstance = None

    # Create a connection with the desired settings
    def createConnection(self) :
        self.connectionInstance = pymysql.connect(host='localhost',
                                user='root',
                                password='root',
                                db='mydb',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor,
                                autocommit=True,
                                connect_timeout=1000)
        print("opening connections")

    # Get an connection that is open or else create a new connection
    def getConnection(self) :
        if self.connectionInstance is None or not self.connectionInstance.open :
            self.createConnection()
        
        return self.connectionInstance

    # Close a connection if one exists
    def closeConnection(self) :
        print("closing connection")
        if self.connectionInstance is not None :
            self.connectionInstance.close()

        self.connectionInstance = None

# instance
connectionHandler = ConnectionHandler()