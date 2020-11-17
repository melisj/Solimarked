
class ShoppingListHandler {
    constructor() {
        this.storageHandler = new StorageHandler();
        this.listNode = document.getElementById('list')
        this.loadList(this.listNode);
    }

    // Load all the lists from the local storage
    loadList(targetList = this.listNode) {
        targetList.textContent = '';
        var products = this.storageHandler.getAll();

        for (var i = 0; i < products.length; i++) {
            this.showItem(products[i], i, targetList);
        }
    }
    
    getList() {
        var products = this.storageHandler.getAll();
        var idObject= {};
        for (var i = 0; i < products.length; i++) {
            var list = [products[i]["idProduct"], products[i]["priceInt"], products[i]["priceFrac"]]
            idObject["id_" + i] = list;
        }
        return idObject;
    }

    sendList(callback) {
        sendXMLRequest("/api/list", "?port=5004", "POST", callback, JSON.stringify(this.getList()))
    }

    clear() {
        this.storageHandler.clear();
        this.loadList(this.listNode);
    }
    
    // Show item off the list
    showItem(product, index, targetList = this.listNode)
    {
        var liNode = document.createElement("LI");
        var txtNode = document.createElement("p");
        txtNode.textContent = product["name"];

        // Create list element
        var buttonElement = document.createElement("Button");
        buttonElement.setAttribute("class", "button_delete_shopping_item");
        buttonElement.setAttribute("onclick", "shoppingListHandler.remove(" + index + ", this.parentElement);");
        buttonElement.textContent = "X";
        
        liNode.appendChild(buttonElement);
        liNode.appendChild(txtNode);
        targetList.appendChild(liNode);
    }

    // Add the new item to the storage
    add(product, index) {
        this.storageHandler.add(product);
        this.showItem(JSON.parse(product), index);
    }
    
    // Delete item from the list
    remove(index, object) 
    {
        this.listNode.removeChild(object);
        this.storageHandler.remove(index);
        this.loadList(this.listNode);
    }
}

class StorageHandler {
    constructor() {
        this.currentCount = 0;
    }

    // Add an item to the storage
    add(product) {
        this.currentCount = this.amount();
        window.localStorage.setItem(this.currentCount, product);
    
        window.localStorage.setItem("count", this.currentCount + 1); 
    }
    
    // Remove one item from the storage and move all the next one index up
    remove(index) {
        this.currentCount = this.amount();

        for(var i = index; i < this.currentCount; i++) {
            window.localStorage.setItem(i, window.localStorage.getItem(i + 1));
        }
        window.localStorage.removeItem(this.currentCount - 1);

        window.localStorage.setItem("count", this.currentCount - 1);
    }
    
    // Clear shopping list in local storage
    clear() {
        this.currentCount = this.amount();
        
        for (var i = 0; i < this.currentCount; i++) {
            window.localStorage.removeItem(i);
        }
        window.localStorage.setItem("count", 0);
    }

    getAll() {
        var returnValue = [];  
        this.currentCount = this.amount();

        for (var i = 0; i < this.currentCount; i++) {
            returnValue.push(JSON.parse(window.localStorage.getItem(i)));
        }
        return returnValue;
    }
    
    // Check the amount of products in the local storage (add one if nesseccary)
    amount() {
        var count = parseInt(window.localStorage.getItem("count"));
        if(Number.isNaN(count))
            window.localStorage.setItem("count", 0); 
        else
            return count;
        return 0;
    }
}