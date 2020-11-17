var groupsUrl = '/api/products/groups';
var categoriesFromGroup = '/api/products/group/categories/'

// Get all the groups from the database
function getAllGroups() {
    sendXMLRequest(groupsUrl,
        '?port=5001',
        'GET',
        showGroups
    );
}

// Get categories for a group
function showCategoriesForGroup(group) {
    sendXMLRequest(categoriesFromGroup + group,
        '?port=5001',
        'GET',
        showCategories
    );
}

// Create elements for the groups
function showGroups(jsonResponse) {
    try {
        var categoryElement = document.getElementById("categories");
        categoryElement.textContent = '';

        jsonResponse.forEach(jsonElement => {
            createCategoryItem(categoryElement, "showCategoriesForGroup(\'" + jsonElement['group'] + "\')", jsonElement['group']);
        });
    }
    catch {

    }
}

// Create elements for the categories
function showCategories(jsonResponse) {
    try {
        var categoryElement = document.getElementById("categories");
        categoryElement.textContent = '';

        jsonResponse.forEach(jsonElement => {
            createCategoryItem(categoryElement, "getProductsWithCategory(\'" + jsonElement['category'] + "\')", jsonElement['category']);
        });
        
        // Add an extra back button
        categoryElement.appendChild(document.createElement("BR"));
        createCategoryItem(categoryElement, "getAllGroups()", "Terug");
    }
    catch {
        
    }
}

// Create a category element and append it to the children
function createCategoryItem(mainElement, onclick, text) {
    var divElement = document.createElement("DIV");
    divElement.setAttribute("class", "category_item");
    divElement.setAttribute("onclick", onclick);

    var linkElement = document.createElement("A");
    linkElement.textContent = cleanString(text);
    divElement.appendChild(linkElement);

    mainElement.appendChild(divElement);
}