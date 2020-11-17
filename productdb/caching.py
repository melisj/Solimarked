from database.query_handler import getGroups, getCategoriesFromGroupName 
import os
import json

# Class for handeling request for groups and categories
# This class will handle the cache of the database to prevent excessive queries to the database.

class CachingHandler() :

    def initializeCache(self) :
        self.saveGroups()
        self.saveCategories()

    # Save to json file
    def saveToFile(self, path, content) :
        with open(path, 'w') as f :
            json.dump(content, f)
            f.close()
    
    # Load json from json file
    # Returns json object
    def loadFile(self, path) :
        with open(path, 'r') as f :
            value = json.load(f)
            f.close()
            return value

    # Function for saving groups
    def saveGroups(self) :  
        self.saveToFile('group_cache.json', getGroups())

    # Function for saving categories in the right format
    def saveCategories(self) :
        dictList = []
        
        for group in getGroups() :
            categoryDict = {
                'group': group['group'],
                'categories': getCategoriesFromGroupName(group['group'])
            }
            dictList.append(categoryDict)

        self.saveToFile('category_cache.json', dictList)

    # Get the groups from the json file
    def getGroups(self) :
        return self.loadFile('group_cache.json')

    # Get the categories in the right format from the file
    def getCategoriesWithGroupName(self, group) :
        result = self.loadFile('category_cache.json')
        for category in result :
            if(category['group'] == group) :
                return category['categories']
        
# instance
cachingHandler = CachingHandler()
