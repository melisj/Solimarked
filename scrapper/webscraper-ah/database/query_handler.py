from database.connection import *

checkForIdQuery = 'SELECT idProduct FROM product WHERE idProduct = %s'
updateProductQuery = 'UPDATE product SET `name` = %s, priceInt = %s, priceFrac = %s, `group` = %s, category = %s, quantity = %s, image = %s WHERE idProduct = %s'
insertProductQuery = 'INSERT INTO product (idProduct, `name`, priceInt, priceFrac, `group`, category, quantity, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

# Check if product should be inserted or updated
def storeProductInDatabase(product) :
    if checkIfInDatabase(product.productId) :
        return updateDatabase(product)
    else :
        return insertIntoDatabase(product)
       
# Check if product can be found in database
def checkIfInDatabase(productId) :
    try :
        with connectionHandler.getConnection().cursor() as cursor:
            cursor.execute(checkForIdQuery, (productId))
            result = cursor.fetchone()
            if result is not None :
                return True
    except pymysql.Error as e :
        print("Error occured in checking database: {}".format(e))
    
    return False

# Update product
def updateDatabase(product) :
    return doUpdateQuery(updateProductQuery, product.getAllItemsForUpdate())

# Add new product
def insertIntoDatabase(product) :
    return doUpdateQuery(insertProductQuery, product.getAllItemsForInsert())

# Function for handling 
def doUpdateQuery(query, parameters) :
    try :
        with connectionHandler.getConnection().cursor() as cursor:
            cursor.execute(query, parameters)
        return True
    except pymysql.Error as e:
        print("Error occured while executing a updating query: {}".format(e))
        return False