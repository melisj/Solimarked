import requests
import time
from tools.string_tool import *
from scraper_data import * 
from scraper_helper import closeScraper, shouldStop

# Scraper class for requesting data and returning data from the raw html string

class Scraper() :
    def __init__(self) :
        # Lists
        self.categoryLinkList = []
        self.subCategoryLinkList = []
        self.productLinkList = []

        # Product info
        self.productList = [] 

        self.currentGroup = ''

    # Collect all the products from the ah product page
    def startCollectingProducts(self) :
        self.categoryLinkList = []
        self.subCategoryLinkList = []
        self.productLinkList = []
        self.productList = [] 

        # Start with the home page
        self.getLinkFromSite(categoryClass, self.categoryLinkList)

        # Get all the sub categories
        for category in self.categoryLinkList :
            self.getLinkFromSite(subCategoryClass, self.subCategoryLinkList, False, category, mobileHeader)
            self.currentGroup = category.split('/')[2]

            # Get all the product links
            for subcategory in self.subCategoryLinkList :
                print()
                self.getLinkFromSite(productClass, self.productLinkList, True, subcategory + amountPageUrl)

                # Debug amount of products retrieved
                print('products retrieved: ' + str(len(self.productLinkList) - info.collectedProducts))
                print('total products: ' + str(len(self.productLinkList)))
                info.collectedProducts = len(self.productLinkList)

            self.subCategoryLinkList.clear()

        return self.productList


    # Load the main product page from albert heijn
    # First check the class tag
    # Then check for the first href and get the url from that
    def getLinkFromSite(self, searchClass, linkList, collectInfo = False, urlPath = '/producten', headers = '') : 
        returnText = requests.get(baseUrl + urlPath, headers=headers).text
        currentIndex = 0

        if collectInfo:
            print(searchClass)
            print(urlPath)

        while currentIndex < len(returnText) :
            if shouldStop() :
                closeScraper()

            try :
                # Find the link in the html
                classIndex = returnText.index(searchClass, currentIndex)
                startLinkIndex = returnText.index(linkString, classIndex) + len(linkString)
                endLinkIndex = returnText.index('"', startLinkIndex)
                link = returnText[startLinkIndex : endLinkIndex]


                # Add link to list and get image from page when specified
                if link not in linkList:
                    linkList.append(link)
                    if collectInfo :
                        self.collectInfoFromProducts(urlPath, link, returnText, endLinkIndex)
                        
                # Check for next link
                currentIndex = endLinkIndex
            except :
                # index function returns error when no links were found (at end of page)
                break
            
        # Debug time and url
        info.currentTime = time.time() - info.startTime
        print('time: ' + str(info.currentTime)[0:6])
        print(urlPath + ' - collected')


    def collectInfoFromProducts(self, urlPath, productUrl, returnText, fromIndex) :
        product = Product()

        self.collectIdAndName(product, productUrl)
        self.collectImage(product, returnText, fromIndex)
        self.collectCategory(product, urlPath)
        self.collectPrice(product, returnText, fromIndex)

        self.productList.append(product)

    def collectIdAndName(self, product, productUrl) :
        # Get product name and id from url
        startIdIndex = productUrl.index(startOfID)
        endIdIndex = productUrl.index('/', startIdIndex)

        # Store the id and the name
        product.setNameAndId(productUrl[startIdIndex : endIdIndex], productUrl[endIdIndex + 1 : len(productUrl)])

    def collectPrice(self, product, returnText, fromIndex) :
        # Get price in integers
        intPrice = getString(returnText, priceClassInt, '</', fromIndex, len(priceClassInt))

        # Get price in decimal numbers
        fracPrice = getString(returnText, priceClassFrac, '</', fromIndex, len(priceClassFrac))

        # Get the quantity of the product
        startQuantityClass = returnText.index(quantityClass, fromIndex)
        quantity = getString(returnText, '>', '</', startQuantityClass, 1)

        product.setPrice(intPrice, fracPrice, quantity)

    # Collect the category of the product from the subcategory url
    def collectCategory(self, product, url) :
        category = getStringReverse(url, '/', '?', 1, 0)
        product.setCategory(category, self.currentGroup)

    # Collect image from the product page
    def collectImage(self, product, returnText, fromIndex) :
        link = getString(returnText, sourceString, '"', fromIndex, len(sourceString))
        
        # Add the base url when image is invalid
        if link[0] == '/' :
            link = baseUrl + link

        product.setImage(link)

scraper = Scraper()