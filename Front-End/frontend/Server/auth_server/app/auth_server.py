from app import app
from flask import Flask, render_template, request, make_response, redirect
import logging as log
import os
import requests
import bleach
import json
import jwt
import datetime


secret_key = "k.asd1234kj1lk24jnmasn1njnananakjsdfjk34"
self_id = "1230912377719237898123981981" 
# Zou van pas komen indien er meerdere auth servers komen.


def decode_cookie(cookie ,local_per, key=secret_key):
        try:
                decoded = jwt.decode(cookie, secret-key)
                if local_per not in dec['per']:
                        return False
                else:
                        return True
        except:
                return False


@app.route('/update-key/auth', methods=['POST'])
def update_key():
        msg = request.get_json()
        key = msg['key']
        return True


@app.route('/login')
def login_screen():
        cookie = request.cookies.get('solimarked-jwt')
        # if cookie:
        #         return redirect('/')
        return render_template('inlog_pagina.html')


@app.route('/login/credentials', methods=['POST', 'GET'])
def cred_call():
        cookie = request.cookies.get('solimarked-jwt')

        # kan aangepast worden naar frontend wensen
        username = bleach.clean(str(request.form['uname'])) 
        password = bleach.clean(str(request.form['passwd']))

        url = "http://solimarked.nl/api"

        r = requests.get(url, params={"username": username, "password": password})


        response = r.text
        # response = json.loads(response)
        if "".join(response.split()) == 0:
                print('Hello')
                return redirect('/login')

        print(response)
        
        # username = response['id']
        # per = response['permissions']
        # user_jwt = jwt.encode({"Usename":username, "per": per}, "Secret-key")
        
        tmp_cookie = jwt.encode({
                "username": username, 
                "per": "TODO", #<- Dit is nu een place holder, moet tuple worden.
                "exp": datetime.datetime.now() + datetime.timedelta(hours=3),
                "sub": username, # Op dit moment kan ik het nog niet db resp parsen
                'iss': self_id
                # 'sub': "" <- Wederom TODO
                }, key=secret_key)

        resp = make_response(render_template('tmp.html'))
        resp.set_cookie('solimarked-jwt', tmp_cookie)
        return resp

        
@app.route('/')
def index():
        cookie = request.cookies.get('solimarked-jwt')
        if not cookie:
                return redirect('/login')

        if not decode_cookie(cookie, "TODO"):
                return redirect('login')
        else:
                return "Index Page"#render_template('index.html')

app.run(host='0.0.0.0', debug=True)

# TODO:
# Momenteel komt de resp van db niet als makkelijk parsebare json. Moet nog een oplossing voor komen.
# Zou wel mooi zijn als er een docker restart command gegeven kan worden, als de server niet reageert.
#
