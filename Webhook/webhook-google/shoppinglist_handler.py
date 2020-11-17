class ShoppingListHandler :
    def __init__(self) :
        self.productList = []
        
    def addEntry(self, product) :
        self.productList.append(product)
    
    def responeListAllEntries(self, sourceValue) :
        if len(self.productList) != 0 :
            opsommingLijstje = ''
            for item in self.productList:
                opsommingLijstje += str(item['name']) + ". "
            
            if "interactieve-handleiding-so-bx" in sourceValue:
                return "Is goed, hier zijn al uw bestelde boodschappen nog een keer op een rijtje. " + opsommingLijstje + ".. Klopt het lijstje zo helemaal?  Dan kunt u bevestigen met ja of weigeren met nee"   
            return "Is goed, hier zijn al uw bestelde boodschappen nog een keer op een rijtje. " + opsommingLijstje + ".. Klopt het lijstje zo helemaal?"
        return "Uw lijst is leeg, voeg producten toe om ze te bestellen."

    def sendToDatabase(self, data, sourceValue) :
        if data == 'ja' :
            if "interactieve-handleiding-so-bx" in sourceValue:
                return "Uw lijstje is dan verstuurt naar het systeem van Solimarked en wordt zo snel mogelijk opgepakt door één van onze vrijwilligers. Dit is het einde van de Solimarket interactieve handleiding, bedankt voor uw deelname."
            return "Uw lijstje is verstuurt naar het systeem van Solimarked."
        return "U kunt nu dan nog verder shoppen. Wat kan ik voor u opschrijven?"

shoppingListHandler = ShoppingListHandler()

