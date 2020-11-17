from database.query_handler import doQuery
import requests

# Script for handleing requests for dialogflow usage
# These functions will request info from the database and translate them to a json format used by dialogflow
# https://cloud.google.com/dialogflow/docs/reference/rest/v2/Entity

# Query for products from category
getProductAsJson = 'SELECT category, `name` FROM product WHERE category = %s LIMIT 23000;'

# Limit of products in synonyms
productLimit = 20

# Get all the products in the database for direct use in the personal assistant application
def getJsonSynonymProducts(category) :
    returnValue = doQuery(getProductAsJson, category)
    productList = []
    for value in returnValue :
        product = value['name']
        if product not in productList :
            productList.append(product)
    
    returnDict = addProductToCategory(productList, category)

    return convertListsToJsonObject(returnDict['lists'], returnDict['category'])

# Limit the amount of synomy entries to max entries (limit of dialogflow per entry = 100)
def addProductToCategory(productList, category) :
    listDict = {
        'lists': [],
        'category': []
    }
    
    index = 0
    amountOfProducts = len(productList)
    print(amountOfProducts)
    
    while index * productLimit < amountOfProducts :
        listDict['lists'].append([])
        listDict['lists'][index] = productList[index * productLimit : (index + 1) * productLimit]
        print(len(listDict['lists'][index]))
        listDict['category'].append(category + str(index))

        index += 1
    
    return listDict

# Convert to the desired json format for dialogflow
def convertListsToJsonObject(productList, category) :
    dictionaryList = []
    for products in productList :
        categoryDict = {
            "synonyms": products,
            "value": category[productList.index(products)]
        }

        dictionaryList.append(categoryDict)

    return dictionaryList
