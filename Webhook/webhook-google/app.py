#!/usr/bin/python3
from flask import Flask, request, abort, jsonify
from flask_restful import Api, Resource
import json
import copy
import requests
from request_handler import requestHandler

app = Flask(__name__)
api = Api(app)

defaultResponse = {
    "payload": {
        "google": {
        "expectUserResponse": True,
        "richResponse": {
            "items": [
                    {
                        "simpleResponse": {
                        "textToSpeech": "De server heeft een fatale fout gemaakt!!!"
                        }
                    }
                ]
            }
        }
    }
}

class GetWebhook(Resource) :
    def post(self) :
        print('\n---------------------------')
        print('Request recieved')

        requestJson = request.get_json()
        response = requestHandler.callIntent(requestJson)

        # Copy default response
        responseDict = copy.deepcopy(defaultResponse)
        textObject = responseDict['payload']['google']['richResponse']['items'][0]['simpleResponse']
        
        if response is not None :
           textObject['textToSpeech'] = response
                
        print('---------------------------\n')
        return jsonify(responseDict)

api.add_resource(GetWebhook, '/api')

if __name__ == '__main__':
    app.run('127.0.0.1', debug=True, port=6000)