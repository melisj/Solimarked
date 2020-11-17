class CacheHandler {
    constructor() {
        this.productCache = null;
        this.productPages = 0;
        this.productCount = 0;
        this.currentPage = 0;
    }

    // Store new product results in the cache
    storeProductCache(results) {
        this.productCache = results;
        this.productPages = Math.floor(results['count'] / results['resultsPerPage']);
        this.productCount = results['count'];
        this.currentPage = 0;
    }
    
    // Get products from the cache with the amount products returned determined by the "resultsPerPage" tag
    // Page starts at 0
    getPageFromProductCache() {
        if(!this.isCacheEmpty()) {
            var resultsPerPage = this.productCache['resultsPerPage'];
            return this.productCache['results'].slice(this.currentPage * resultsPerPage, this.currentPage * resultsPerPage + resultsPerPage);
        }
        return null
    }

    // Get the last query that is stored in cache
    getLastQuery() {
        return (this.productCache != null) ? this.productCache['query'] : ' ';
    }

    // Check if the cache is empty
    isCacheEmpty() {
        if(this.productCache != null)
            return this.productCache['count'] == 0;
        else
            return true;
    }
}

var cacheHandler = new CacheHandler();