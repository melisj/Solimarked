class HandleidingHandler :

    def confirmUseHandleiding(self, data, sourceValue) :
        if data == 'start de handleiding' and "interactieve-handleiding-so-bx" in sourceValue:   
            return "Welkom bij de interactieve handleiding van Solimarket. Bij deze handleiding nemen we u mee in het bestel process. Om te begrijpen welke producten u wilt bestellen is het nodig voor ons systeem dat u de specifieke namen van de producten die u wilt bestellen opnoemt. Bijvoorbeeld om een heel bruin tijger brood te bestellen, zegt u ah tijger bruin heel. Laten we dat eens proberen."

    def getProduct(self,query) :
            if query is not '' and query is not None :
                return "Is " + query + " het product wat u zoekt? Laten we voor nu het product toevoegen aan het boodschappenlijstje. Dan kunt u bevestigen met ja of weigeren met nee. "

    def confirmProductHandleiding(self, data, shoppingListHandler, productHandler) :
        shoppingListHandler.addEntry(productHandler.currentProduct)
        return  "{} is toegevoegt aan uw lijstje! Als u het opgestelde lijstje wilt beluisteren kunt u herhaal mijn boodschappenlijstje inspreken of als u nog een product wilt bestellen kunt u dat voortaan hier inspreken, laten we voor nu naar het boodschappenlijstje luisteren".format(productHandler.currentProduct['name'])

handleidingHandler = HandleidingHandler()