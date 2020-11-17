import requests
from handleiding_handler import handleidingHandler


class ProductHandler :
    cleanQueryList = {'ah', 'basic'}
    seperationChar = '-'

    databaseUrl = "http://ahscraper.duckdns.org:5001/api/products/search?name="

    def __init__(self) :
        self.currentProduct = None

    def getProduct(self, query, sourceValue) : 
        result = self.makeRequestToDatabase(self.getKeyWordsFromRequest(query))
        
        if "interactieve-handleiding-so-bx" in sourceValue:
            return handleidingHandler.getProduct(result)

        # Add result into the string
        if result is not '' and result is not None :
            return "Is " + result + " het product wat u zoekt?"
        return "We hebben helaas niks kunnen vinden."


    def getKeyWordsFromRequest(self, query) :
        if query == '' :
            return None

        query = query.replace(' ', self.seperationChar).lower()
        
        wordList = query.split(self.seperationChar)
        wordList.append(query)
        
        keywords = []
        for word in wordList :
            word = word.replace(self.seperationChar, ' ').strip()
            # Check if word should be searched
            if word not in self.cleanQueryList :
                keywords.append(word.strip(' '))

        print(keywords)
        return keywords

    # Make for each keyword a request and get the request with the least amount of results
    def makeRequestToDatabase(self, keywords) :
        lowestValue = 1000
        results = None
        if keywords is not None :
            for word in keywords :
                returnValue = requests.get(self.databaseUrl + word).json()
                count = returnValue['count']

                # Get the shortest correct result
                if min(count, lowestValue) is not lowestValue and count is not 0:
                    lowestValue = count
                    results = returnValue

        return self.getBestResult(results)

    # Get the best result out of the response of the database
    def getBestResult(self, results) :
        if results is not None :
            bestResult = None
            if results['count'] > 1 :
                shortestValue = 1000

                for product in results['results'] :
                    nameLength = len(product['name'])
                    if min(nameLength, shortestValue) is not shortestValue :
                        shortestValue = nameLength
                        bestResult = product 
            else :
                bestResult = results['results'][0]
            
            self.currentProduct = bestResult
            return bestResult['name'].replace(self.seperationChar, ' ')
        return None

    # Confirm product
    def confirmProduct(self, data, shoppingListHandler, productHandler, sourceValue) :
        if data == 'ja' :
            if "interactieve-handleiding-so-bx" in sourceValue:
                return handleidingHandler.confirmProductHandleiding(productHandler.currentProduct, shoppingListHandler, productHandler)
            
            if self.currentProduct is not None :
                shoppingListHandler.addEntry(productHandler.currentProduct)
                return  "{} is toegevoegt aan uw lijstje! Welk product kan ik nog meer voor u opschrijven?".format(self.currentProduct["name"])
        return "{} is niet toegevoegt, Welk product kan ik dan voor u opschrijven?".format(self.currentProduct["name"])

productHandler = ProductHandler()
