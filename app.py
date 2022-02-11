from math import prod
from flask import Flask, jsonify, request
from itsdangerous import json
app = Flask(__name__)

from data import data

@app.route('/ping')
def ping():
    return jsonify({"message": "pong"})

@app.route('/products')
def products():
    return jsonify({"products": data})

@app.route('/products/<string:product_name>')
def getProduct(product_name):
    productFound = [product for product in data if product['name'] == product_name ]
    if(len(productFound) >0):
        return jsonify({"product": productFound[0]})
    return jsonify({"message": "Product not found"})

@app.route('/products', methods = ['POST'])
def addProduct():
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    data.append(new_product)

    return jsonify({"message": "Product added", "products": data})
    #Reciving data from the body

@app.route('/products/<string:product_name>', methods = ['PUT'])
def updateProduct(product_name):
    productFound = [product for product in data if product['name'] == product_name]
    if(len(productFound) > 0):
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
    
    return jsonify({
        "message": "Product updated succesfully",
        "products": data
    })

@app.route('/products/<string:product_name>', methods= ['DELETE'])
def deleteProduct(product_name):
        productFound = [product for product in data if product['name'] == product_name]
        if(len(productFound) > 0):
            data.remove(productFound[0])
            return jsonify({
                "message": "Element removed succesfully",
                "products": data
            })
        else:
            return jsonify({
                "message": "This product name is not in our inventory"
            })

if __name__ == "__main__":
        app.run(debug =  True, port = 5000)