from scraper import scraper
from database.query_handler import storeProductInDatabase
from database.connection import connectionHandler
from scraper_data import Product, ScraperStatus, ScraperInfo, info
from scraper_helper import setStatus, shouldStop, checkStatus, closeScraper
import time

# Script for managing the flow of the process

# Function to start scraping
# Will collect products from ah and store them in the database
def scrapeAlbertHeijn() :
    if checkStatus() :
        # Set info
        info.reset()
        setStatus(ScraperStatus.running)

        try : 
            # Get all the products from the albert heijn
            productList = scraper.startCollectingProducts()

            # Finish product collection
            printCollectedProducts()

            storeProductsInDatabase(productList)

            # End connection
            endProcess()

        # Scraper failed
        except (RuntimeError, TypeError, NameError) as e:
            print('scraper failed! {}'.format(e))

        # Scraper is done
        setStatus(ScraperStatus.stopped)
        print('scraper is done')
    else :
        # Scraper is busy
        print('\nscraper is already busy\n')

# Store the collected products
def storeProductsInDatabase(productList) :
    print('products are going to be stored in the database, this can take a couple of minutes \n')
    setStatus(ScraperStatus.storingInDatabase)

    # Store all the products in the database
    for product in productList :
        if shouldStop() :
            closeScraper()

        if storeProductInDatabase(product) :
            info.productStored += 1

def printCollectedProducts() :
    print('\n---------------------------------------------------------')
    print('total products collected: ' + str(info.collectedProducts))
    print('total time: ' + str(time.time() - info.startTime))
    print('---------------------------------------------------------\n')

def endProcess() :
    print('storing results done')
    print('\n---------------------------------------------------------')
    print('total time it took: {}'.format(time.time() - info.startTime))
    print('products stored in database: {}/{}'.format(str(info.productStored), str(info.collectedProducts)))
    print('---------------------------------------------------------\n')

    connectionHandler.closeConnection()