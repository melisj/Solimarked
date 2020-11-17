#!/usr/bin/python3

from flask import Flask, request, abort, jsonify
from flask_restful import Api, Resource
from database.query_handler import getCategories, getProduct, searchProductFromCategory, searchProductsWithName, searchProductFromGroup, getCategories
from database.personal_assistant_converter import getJsonSynonymProducts
from caching import cachingHandler
import codecs

app = Flask(__name__)
api = Api(app)

cachingHandler.initializeCache()

# Check if the arguments are defined
def checkForValidArguments(arg) :
    if not arg == '' and arg is not None :
        return arg
    else :
        abort(400, 'bad request, arguments are not defined')

# Used for converting category results to json for dialoglfow
class GetJsonFromCategory(Resource) :
     def get(self, category) :
        return jsonify(getJsonSynonymProducts(category))

# /api/products/groups returns all the groups
class GetGroups(Resource) :
    def get(self) :
        return cachingHandler.getGroups()

# /api/products/categories returns all the available product categories
class GetCategories(Resource) : 
    def get(self) :
        return jsonify(getCategories())

# /api/products/group/categories/<group> returns all the categories within a group
class GetCategoriesFromGroup(Resource) :
    def get(self, group) :
        return cachingHandler.getCategoriesWithGroupName(group)

# /api/products/product/<idProduct> returns product info for the given id
class GetProduct(Resource) :
    def get(self, idProduct) :
        return jsonify(getProduct(idProduct))

# /api/products/search?name=[part of name] returns product info from product which contain the given name
class SearchProducts(Resource) :
    def get(self) :
        name = checkForValidArguments(request.args.get('name'))
        return jsonify(searchProductsWithName(name))

# /api/products/category/<category>?sortby=[sortby(price,name)] returns all products within a category, sorted by default with name. 
class ProductsFromCategory(Resource) :
    def get(self, category) :
        sortby = checkForValidArguments(request.args.get('sortby'))
        return jsonify(searchProductFromCategory(category, sortby))

# /api/products/group/product/<group>?sortby=[sortby(price,name)] returns all products within a group, sorted by default with name. 
class ProductsFromGroup(Resource) :
    def get(self, group) :
        sortby = checkForValidArguments(request.args.get('sortby'))
        return jsonify(searchProductFromGroup(group, sortby))

api.add_resource(GetGroups, '/api/products/groups')
api.add_resource(GetCategoriesFromGroup, '/api/products/group/categories/<group>')

api.add_resource(GetProduct, '/api/products/product/<idProduct>')
api.add_resource(SearchProducts, '/api/products/search')
api.add_resource(ProductsFromCategory, '/api/products/category/<category>')
api.add_resource(ProductsFromGroup, '/api/products/group/product/<group>')

# For the google home api
api.add_resource(GetJsonFromCategory, '/api/products/json/<category>')
api.add_resource(GetCategories, '/api/products/json/all')

if __name__ == '__main__':
    app.run('192.168.1.94', debug=False, port=5001)


