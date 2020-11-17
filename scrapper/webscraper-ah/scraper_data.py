import enum
import time

# Basic ah url
baseUrl =  'https://www.ah.nl'

# Do request with mobile headers to return the page so the food categories are all send in the html
mobileHeader = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}

# Classes
categoryClass = 'class="product-category-overview_category__E6EMG"'
subCategoryClass = 'class="taxonomy-sub-selector_child__1yS69"'
productClass = 'class="product-card-portrait_root__M_ldz product-grid-lane_gridItem__23YH5"'

priceClassInt = 'class="price-amount_integer__2Vidn">'
priceClassFrac = 'class="price-amount_fractional__iOz4d">'
quantityClass = 'class="price_unitSize__3vj0T"'

# Tags
linkString = 'href="'
sourceString = 'src="'
amountPageUrl = '?page=100'
startOfID = 'wi'

class Product() :
    productId = ''
    name = ''
    category = ''
    group = ''
    priceInt = 0
    priceFrac = 0
    quantity = ''
    imageUrl = ''

    def setPrice(self, priceInt, priceFrac, quantity) :
        self.priceInt = priceInt
        self.priceFrac = priceFrac
        self.quantity = quantity

    def setNameAndId(self, productId, name) :
        self.productId = productId
        self.name = name

    def setImage(self, imageUrl) :
        self.imageUrl = imageUrl

    def setCategory(self, category, group) :
        self.category = category
        self.group = group

    # Return product for storage in the database
    def getAllItemsForInsert(self) :
        return (self.productId, self.name, int(self.priceInt), int(self.priceFrac), self.group, self.category, self.quantity, self.imageUrl)
        
    def getAllItemsForUpdate(self) :
        return (self.name, int(self.priceInt), int(self.priceFrac), self.group, self.category, self.quantity, self.imageUrl, self.productId)

# Enum class for the status
class ScraperStatus(enum.Enum) :
    stopped = 0
    running = 1
    storingInDatabase = 2
    stopping = 3

# Info about the scraper used to manage the process
class ScraperInfo() :
    status = ScraperStatus.stopped
    collectedProducts = 0
    productStored = 0
    shouldBeStopping = False
    startTime = 0
    currentTime = 0

    def reset(self) :
        self.startTime = time.time()
        self.productStored = 0
        self.collectedProducts = 0
        self.shouldBeStopping = False
        self.currentTime = 0

info = ScraperInfo()