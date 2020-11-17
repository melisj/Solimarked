

# Product Database


### Description

De product database server handelt alle requests af voor het ophalen van producten uit het database. De producten van de database komen van de albert heijn en bevat ongeveer 21000 producten. 

De server is er alleen om get requests te ontvangen van de gebruiker en kan zelf dus niks aan het database veranderen.

The server kan maximaal 500 resultaten terug geven met een request.


### Prerequisites



*   Python 3


### Installation



1. Clone repository 
2. Command pip install -r requirements.txt
3. Python app.py
*   Runs on port 5001


### End points

De endpoints van de server worden hieronder beschreven met de verschillende return values. Alle endpoints geven json terug.

**/api/products/groups: **haalt alle groepen van het database op, returned een lijst met groepen terug.

[

	{“group” : “(group-name)”},

	…

]

**/api/products/group/categories/&lt;group>:** geeft alle categorieën terug die bij de groep horen die is meegegeven in de url.

[

	{“category” : “(category-name)”},

	…

]	

**/api/products/product/&lt;product id>:** geeft informatie terug over een product met alle velden van het database.

{

  "category": "vruchtensappen-en-drank", 

  "group": "frisdrank-sappen-koffie-thee", 

  "idProduct": "wi100845", 

  "image": "https://static.ah.nl/image-optimization/static/product/AHI_43545239363034363738_1_200x200_JPG.JPG?options=399,q85", 

  "name": "ah-gekoeld-sinaasappeldrank", 

  "priceFrac": 59, 

  "priceInt": 1, 

  "quantity": "1 l"

}

**/api/products/product/search?name=””:** request om te zoeken naar producten in het database met een bepaalde naam of deel van naam. Name value moet gegeven zijn.

{

  "count": 6, 

  "query": "alpro", 

  "results": [ &lt;resultaten hier> ], 

  "resultsPerPage": 8, 

  "type": "name"

}

count = hoeveelheid resultaten

query = gegeven query value

results = producten lijst met alle informatie van de producten

resultsPerPage = is een setting die in het database is aan te passen en kan gebruikt worden op de front end om de hoeveelheid resultaten per pagina te bepalen.

type = type request, mogelijke waardes: “name”, “category” en “group”

**/api/products/category/&lt;category>?sortby=””:** request om alle producten van een category op te halen. Hierbij worden de producten ook gesorteerd, standaard op naam, maar dit kan ook op prijs, door sortby=price. anders moet er staan sortby=name.

{

  "count": 246, 

  "query": "fruit", 

  "results": [ &lt;resultaten hier> ], 

  "resultsPerPage": 8, 

  "type": "category"

}

Not used:

**/api/products/group/products/&lt;group>?sortby=””:** zelfde als vorige maar dan met groepen in plaats van categoriën.

{

  "count": 500, 

  "query": "aardappel-groente-fruit", 

  "results": [ &lt;resultaten hier> ], 

  "resultsPerPage": 8, 

  "type": "group"

}


### Database content

Een product bevat een aantal velden die gebruikt kunnen worden binnen een applicatie. 

De velden worden hieronder beschreven.

Product:



*   idProduct: een product heeft een id met het volgende format: ”wi + max 6 nummers” bijv: “wi100845” 
*   name: complete naam van het product (met “-” als spaties).
*   group: de overkoepelende categorie waarin de producten zitten.
*   category: de specifieke categorie van het product.
*   price: de prijs van het product is verdeeld in twee, hierbij is er priceInt en de priceFrac. priceInt is voor hele euro’s en priceFrac voor de centen. Allebei zijn dit integer values.
*   quantity: de hoeveelheid van het product voor de gegeven prijs.
*   image: url voor het plaatje van het product.