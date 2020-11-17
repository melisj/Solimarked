from database.db_connection import pymysql, connectionHandler
import math

getAllGroups = 'SELECT `group` FROM product GROUP BY `group` ORDER BY `group`;'
getAllCategoriesFromGroup = 'SELECT category FROM product WHERE `group` = %s GROUP BY category ORDER BY category;'
getAllCategories = 'SELECT category FROM product GROUP BY category ORDER BY category;'

getProductsFromCategory = 'SELECT * FROM product WHERE category = %s ORDER BY %s LIMIT 500;'
getProductsFromGroup = 'SELECT * FROM product WHERE `group` = %s ORDER BY %s LIMIT 500;'
getProductsFromName = 'SELECT * FROM product WHERE `name` LIKE %s LIMIT 500;'
getProductFromId = 'SELECT * FROM product WHERE idProduct = %s;'

sortbyName = '`name`'
sortbyPrice = 'priceInt, priceFrac'
productsPerRequest = 8

# Return first product with the given id
def getProduct(idProduct) :
    return doQuery(getProductFromId, idProduct)[0]

def getWhichSortToBeUsed(sortby) :
    return sortbyPrice if sortby.lower() == 'price' else sortbyName

# Get all products from a category
def searchProductFromCategory(category, sortby) :
    results = doQuery(getProductsFromCategory, [category, getWhichSortToBeUsed(sortby)])    
    return packResultsIntoJson(results, len(results), 'category', category)

# Get all products from a group
def searchProductFromGroup(group, sortby) :
    results = doQuery(getProductsFromGroup, [group, getWhichSortToBeUsed(sortby)])    
    return packResultsIntoJson(results, len(results), 'group', group)

# Search for a product with the given name as a specifier
def searchProductsWithName(name) : 
    # Add the wildcards to the query
    nameString = '%' + name.replace(' ', '%').replace('-', '%') + '%'
    results = doQuery(getProductsFromName, nameString)  
    return packResultsIntoJson(results, len(results), 'name', name) 

# Get categories from the database
def getCategories() :
    return doQuery(getAllCategories)

# Get categories from the database
def getGroups() :
    return doQuery(getAllGroups)

# Get categories within a specific group
def getCategoriesFromGroupName(group) :
    return doQuery(getAllCategoriesFromGroup, group)

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

# Return multiple results in a json file
def packResultsIntoJson(results, count, typeReq, query) :
    return {
        'results' : results, # Results from database
        'count' : count, # Amount of results
        'resultsPerPage' : productsPerRequest, # Products that should be shown per page
        'type' : typeReq, # The type of request ("name", "group", "category")
        'query' : query # The original query
    }