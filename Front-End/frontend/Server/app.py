#!/usr/bin/python3

from flask import Flask, request, abort, jsonify, send_file, redirect
from flask_restful import Api, Resource
import codecs
import requests
from jwt_token import jwt_Token

nep_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib29kc2NoYXBwZW5saWpzdGplIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.T_PAPTAccQ4r9aLCjJedx1WyacfQpUAtmRor2A5j8N0"

app = Flask(__name__)
api = Api(app)

redirectPath = 'http://ahscraper.duckdns.org:'

def parse_token(cookie=False):
    try:
        tmp = jwt_Token(cookie, 'Secret-Key', "boodschappenlijstje").check_service()
        return tmp
    except Exception as e:
        print(e)
        

def sendHTML(name) :
    f = open('frontend/html/' + name + '.html', 'r')
    response = app.make_response(f.read())
    response.headers['Content-Type'] = "text/html"
    response.set_cookie('solimarket', nep_token)

    return response  

class RedirectQuery(Resource) :
    def get(self) :
        try :
            return jsonify(requests.get(redirectPath + request.args.get("port") + request.full_path).json())
        except : 
            abort(401)
    def post(self) :
        try :
            return requests.post(redirectPath + request.args.get("port") + request.full_path, data=request.data).text
        except : 
            abort(401)
    def delete(self) :
        try :
            return requests.post(redirectPath + request.args.get("port") + request.full_path).text
        except : 
            abort(401)

class RedirectQueryWithParam(Resource) :
    def get(self, param) :
        print(request.full_path)
        try :
            return jsonify(requests.get(redirectPath + request.args.get("port") + request.full_path).json())
        except : 
            abort(401) #return sendHTML('inlog_pagina')

class GetHTML(Resource) :
    def get(self, html) :
        print(html)
        return sendHTML(html)

class GetCss(Resource) :
    def get(self, file) :
        f = open('frontend/css/' + file, 'r')
        response = app.make_response(f.read())
        response.headers['Content-Type'] = "text/css"
        return response

class GetJs(Resource) :
    def get(self, file) :
        f = open('frontend/javascript/' + file, 'r')
        response = app.make_response(f.read())
        response.headers['Content-Type'] = "text/javascript"
        return response

class GetFile(Resource) :
    def get(self, file) :
        extension = request.args.get('extension')
        return send_file('frontend/resources/' + file + '.' + extension, mimetype="image/png")

class RedirectToMain(Resource) :
    def get(self) :
        return redirect(redirectPath + "5002" + "/html/product_page")

api.add_resource(RedirectQuery, '/api/products/categories', '/api/products/search', '/api/products/groups', '/api/list', "/lijstje/display", "/lijstje/items", "/lijstje/delete")
api.add_resource(RedirectQueryWithParam, '/api/products/category/<param>', '/api/products/product/<param>', '/api/products/group/categories/<param>', '/api/products/group/product/<param>')
api.add_resource(GetCss, '/frontend/css/<file>')
api.add_resource(GetJs, '/frontend/javascript/<file>')
api.add_resource(GetHTML, '/html/<html>')
api.add_resource(GetFile, '/resources/<file>')
api.add_resource(RedirectToMain, '/')

if __name__ == '__main__':
    app.run('192.168.1.94', debug=True, port=5002)