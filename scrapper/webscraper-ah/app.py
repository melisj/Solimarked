#!/usr/bin/python3

from flask import Flask
from flask_restful import Api, Resource, abort
from scraper_manager import scrapeAlbertHeijn
from scraper_helper import stopScraper, getStatus
from threading import Thread

app = Flask(__name__)
api = Api(app)

class StartScraper(Resource) : 
    def get(self) :
        Thread(target=scrapeAlbertHeijn).start()
        return 'started'

class StopScraper(Resource) : 
    def get(self) :
        stopScraper()
        return 'stopping'

class GetStatusScraper(Resource) : 
    def get(self) :
        return getStatus()

api.add_resource(StartScraper, '/api/scraper/start')
api.add_resource(StopScraper, '/api/scraper/stop')
api.add_resource(GetStatusScraper, '/api/scraper/status')

if __name__ == '__main__':
    app.run('0.0.0.0', debug=False, port=5005)

# TODO Cleanup code