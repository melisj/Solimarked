from scraper_data import info, ScraperStatus
import sys 

# Function for controlling the status of the scraper

# Returns whether scraper is busy
def checkStatus() :
    return info.status == ScraperStatus.stopped

def setStatus(newStatus) :
    info.status = newStatus
    return info.status

def getStatus() :
    return str(info.status)

# Sets flag for the system to stop the scraper 
def stopScraper() :
    if info.status == ScraperStatus.running :
        info.shouldBeStopping = True
        setStatus(ScraperStatus.stopping)

def shouldStop() :
    return info.shouldBeStopping

# Close the thread and set the status
def closeScraper() :
    print('scraper has stopped')
    setStatus(ScraperStatus.stopped)
    sys.exit()