var domainName = 'http://ahscraper.duckdns.org:5002'

// Keep track of which requests are made to the database
// This prevents it from sending multiple requests to the same address with the same request
var requestList = []

// Send requests to the server for information
function sendXMLRequest(url, requestParams, requestType, callback = null, variables = '') {
    if(!requestList.includes(url)) {
        var xml = new XMLHttpRequest();
        xml.open(requestType, domainName + url + requestParams);
        requestList.push(url);

        xml.onreadystatechange = () => {
            if(xml.readyState == 4 && xml.status >= 200 && xml.status <= 400){
                // Success
                if (callback != null) {
                    callback(JSON.parse(xml.responseText));
                    deleteFromRequestList(url);
                }
            }
            // Error
            else if (xml.status < 200 || xml.status > 400)
                deleteFromRequestList(url);
            
        };
        
        // Error
        xml.onabort = xml.ontimeout = xml.onerror = deleteFromRequestList(url);

        xml.send(variables);
    }
    else {
        console.log("Requests where too close too each other")
    }
}

// Request was finshed or terminated
function deleteFromRequestList(url) {
    index = requestList.indexOf(url);

    if(index != -1)
        requestList.splice(index, 1);
}