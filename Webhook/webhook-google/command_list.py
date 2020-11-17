from product_handler import productHandler
from shoppinglist_handler import shoppingListHandler
from handleiding_handler import handleidingHandler

def confirmUseHandleiding(data) :
    return handleidingHandler.confirmUseHandleiding(data['entityValue'], data['source'])

def getProductFromName(data) :
    return productHandler.getProduct(data['entitySynonym'], data['source'])

def confirmProduct(data) :
    return productHandler.confirmProduct(data['entityValue'], shoppingListHandler, productHandler, data['source'])

def boodschappenlijstjeHerhalen(data) :
    return shoppingListHandler.responeListAllEntries(data['source'])

def sendShoppingListToDatabase(data) :
    return shoppingListHandler.sendToDatabase(data['entityValue'], data['source'])



intentList = [
    'bestel ',
    '- confirmation',
    'boodschappenlijstje herhalen',
    'stuur lijstje',
    'confirmationHandleiding',
    'boodschappenlijstje herhalen hand'
]

functionList = [    
    getProductFromName,
    confirmProduct,
    boodschappenlijstjeHerhalen,
    sendShoppingListToDatabase,
    confirmUseHandleiding
]
