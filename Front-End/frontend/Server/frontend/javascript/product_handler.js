queryUrl = '/api/products/search';
categoryUrl = '/api/products/category/'

var queryForm = null

var buttonUp = null;
var buttonDown = null;
var buttonPanel = null;
var resultDisplay = null;
var shoppingContent = null;
var tableElement = null;

var productsPerRow = 4;

// Get all the elements form the page
function initForm() {
    queryForm = document.getElementById("query_form");
    buttonUp = document.getElementById('page_up_button');
    buttonDown = document.getElementById('page_down_button');
    buttonPanel = document.getElementById('page_selector');
    resultDisplay = document.getElementById('result_display');
    shoppingContent = document.getElementById('shopping_content');
    tableElement = document.getElementById("product_table");

    resizeTable();
    queryForm.addEventListener("submit", catchProductSearch)
    window.addEventListener("resize", resizeTable);

    updatePageVisuals();
}

// Catch the form event where the user types an query
function catchProductSearch(event) {
    event.preventDefault();
    query = queryForm.query_field.value;
    query.trim();

    getProductsWithName(query);
}

// Get products from database with name
function getProductsWithName(name) {
    if(name != '')
        sendXMLRequest(queryUrl,
            '?name=' + name + "&port=5001", 
            'GET',
            retrieveProducts
        );
}

// Get products from database with category
function getProductsWithCategory(category) {
    sendXMLRequest(categoryUrl + category,
        '?sortby=price' + "&port=5001", 
        'GET',
        retrieveProducts
    );
}

// Callback for recieving products and showing the results
function retrieveProducts(results) {
    // Store the 
    cacheHandler.storeProductCache(results);

    pageResult = cacheHandler.getPageFromProductCache();
    

    showProducts(pageResult);

    updatePageVisuals();
}

// Create elements which will contain the products
function showProducts(results) {
    console.log(results);
    tableElement.textContent = '';

    var currentTableRow = null;

    if(results != null)
        results.forEach((element, index) => {
            if (index % productsPerRow == 0)
                currentTableRow = tableElement.insertRow(Math.floor(index / productsPerRow));
            
            createProductElement(element, currentTableRow);
        });
}

function createProductElement(productInfo, tableRowElement) {
    var tableColumnElement = document.createElement("td");
    tableColumnElement.setAttribute("class", "product");

    // Create image element
    imageElement = document.createElement("img");
    imageElement.setAttribute("src", productInfo['image']);
    tableColumnElement.appendChild(imageElement);

    // Create price and quantity element
    priceElement = document.createElement("p");
    priceElement.setAttribute("class", "product_price");
    priceElement.textContent = "\u20AC" + productInfo['priceInt'] + "." + productInfo['priceFrac'] + " || " + productInfo['quantity'];
    tableColumnElement.appendChild(priceElement);

    // Create buy button
    buyElement = document.createElement("button");
    buyElement.setAttribute("onclick", "shoppingListHandler.add(\'" + JSON.stringify(productInfo) + "\', shoppingListHandler.storageHandler.amount());");
    buyElement.textContent = "Koop";
    tableColumnElement.appendChild(buyElement);

    // Create text element for the name of the product
    nameElement = document.createElement("div");
    nameElement.setAttribute("class", "product_name");
    nameElement.textContent = cleanString(productInfo['name']);
    tableColumnElement.appendChild(nameElement);

    tableRowElement.appendChild(tableColumnElement);
}

// Page Selector Functionality
// --------------------------------------------------------------------------------------------------

// Function called when a new product page is requested
function changePage(increment) {
    if (capPage(cacheHandler.currentPage, increment)) 
        changeProducts();
}

// Show new products when the products were changed 
function changeProducts() {
    showProducts(cacheHandler.getPageFromProductCache());
    updatePageVisuals();
}

// Cap page num between max and min
// Returns whether it has been changed or not
function capPage(page, increment) {
    newPage = page + increment;
    if(newPage < 0 || newPage > cacheHandler.productPages) {
        return false;
    }
    cacheHandler.currentPage = newPage;
    return true;
}

// Update the visual aspect of the page selector
// Update text about the query made
function updatePageVisuals() {
    if(!cacheHandler.isCacheEmpty()){
        buttonPanel.style.visibility = cacheHandler.productCount == 1 ? 'hidden' : 'visible';
        buttonDown.style.visibility = cacheHandler.currentPage <= 0 ? 'hidden' : 'visible';
        buttonUp.style.visibility = cacheHandler.currentPage >= cacheHandler.productPages ? 'hidden' : 'visible';

        document.getElementById('page_counter').textContent = cacheHandler.currentPage + 1;
    }
    else 
        buttonPanel.style.visibility = 'hidden';

    // Show latest query made
    resultDisplay.textContent = cleanString(cacheHandler.getLastQuery());
}

// Table handler (resize table when the window shrinks or grows)
function resizeTable() {
    size = shoppingContent.getBoundingClientRect()['width'] * 0.7;
    amountOfProductsInRow = Math.floor(size / 204);

    amountOfProductsInRow = Math.max(1, amountOfProductsInRow)
    productsPerRow = amountOfProductsInRow;
    if(!cacheHandler.isCacheEmpty())
        showProducts(cacheHandler.getPageFromProductCache());
}
