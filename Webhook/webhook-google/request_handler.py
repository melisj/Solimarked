from command_list import intentList, functionList

class RequestHandler :
    # Call the matching intent name and call the assigned function
    def callIntent(self, data) :
        requestIntent = self.getIntent(data)
        queryvalues = data['queryResult']['outputContexts'][0]['parameters']
        sourceValue = data['queryResult']['outputContexts'][0]['name']
        entityName = self.getContext(queryvalues)

        customData = {
            'entityValue' : queryvalues[entityName] if entityName is not None else '',
            'entitySynonym' : queryvalues['{}.original'.format(entityName)] if entityName is not None else '',
            'source' : sourceValue if entityName is not None else ''
        }
        print(customData)

        for intent in intentList :
            if intent in requestIntent :
                return functionList[intentList.index(intent)](customData)
        return None
   
    # Get the current entities variables
    def getContext(self, data) :
        for variable in data :
            if data[variable] is not '' :
                return variable

    # Get source intent from the json
    def getIntent(self, data) : 
        return data['queryResult']['intent']['displayName']


requestHandler = RequestHandler()
