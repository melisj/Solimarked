#!/usr/bin/python3

from flask import Flask, request, abort, jsonify, render_template
from database.query_handler import doQuery
import json

app = Flask(__name__, template_folder="./")


# Check if the arguments are defined
def checkForValidArguments(arg) :
    if not arg == '' and arg is not None :
        return arg
    else :
        abort(400, 'bad request, arguments are not defined')


@app.route("/lijstje/items", methods = ["GET"])
def getItems() :
    args_id = request.args.get("id")
    getIds = doQuery(f"SELECT product_idProduct, amount FROM shoppinglist_has_product WHERE shoppinglist_user_id = 3412 AND shoppinglist_id = {args_id}")

    list_total = []
    for idx in getIds:
       list_total.extend(doQuery(f'SELECT `name` FROM product WHERE idProduct = \'{idx["product_idProduct"]}\''))
    
    listObject = {
        "list": list_total,
        "cost": doQuery(f'SELECT total_cost FROM shoppinglist WHERE id = {args_id}')[0]["total_cost"]
    }

    return jsonify(listObject)


@app.route("/lijstje/delete", methods = ["GET", "POST", "PUT", "DELETE"])
def del_lijst():
    try:
        list_to_be_deleted = request.args.get("id")
        del_string = f"DELETE FROM shoppinglist WHERE id='{list_to_be_deleted}'"

        if doQuery(del_string):
            return "200"
        else:
            return "500"
    except Exception as e:
        return "500"


@app.route("/lijstje/display", methods = ["GET"])
def getLists() :
    return jsonify(doQuery("SELECT * FROM shoppinglist WHERE user_id = 3412"))


@app.route("/api/list", methods=["GET", "POST"])
def postList():
    product_json = json.loads(request.data)
    priceInt = 0
    priceFrac = 0

    # Get duplicates from ids and store total price
    duplicate = {}
    for idx in product_json:
        id = product_json[idx][0]
        if id in duplicate:
            duplicate[id] += 1
        else:
            duplicate[id] = 1
        
        priceInt += product_json[idx][1]
        priceFrac += product_json[idx][2]

    # Get total price of products
    priceInt += priceFrac // 100
    priceFrac %= 100  
    
    totalCost = f"{priceInt}.{priceFrac}" 
    
    # Create shoppinglist and get it
    doQuery(f"INSERT INTO shoppinglist (user_id, total_cost) VALUES(3412, {totalCost})")
    latestAndGreatest = str(doQuery("SELECT id FROM shoppinglist WHERE user_id=3412 ORDER BY id DESC LIMIT 1;")[0]["id"])

    # Store all products in database
    for prod in duplicate:
        insert_string = f"""INSERT INTO shoppinglist_has_product
(shoppinglist_id, shoppinglist_user_id, product_idProduct, amount) VALUES 
({latestAndGreatest}, 3412,'{str(prod)}', {duplicate[prod]})"""
        doQuery(insert_string)

    return ("", 200)


@app.route("/lijstje/shopper", methods = ["GET"])
def claim_list():
    if request.args.get("claimed"):
        claimed_list = request.args.get("claim")
    else:
        return "", 400

    
    
    
    
    print()
    return "", 200    

if __name__ == '__main__':
    app.run('192.168.1.94', debug=True, port=5004)
