from flask import Flask,render_template,request,jsonify,redirect, url_for, g,send_from_directory
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import logging
import sys
import datetime
import bcrypt
import traceback

from psycopg2 import sql
from db_con import get_db_instance, get_db

from tools.token_required import token_required
from tools.get_aws_secrets import get_secrets

from tools.logging import logger

ERROR_MSG = "Ooops.. Didn't work!"


#Create our app
app = Flask(__name__)
#add in flask json
FlaskJSON(app)


global_db_con = get_db()

#g is flask for a global var storage 
def init_new_env():
    if 'db' not in g:
        g.db = get_db()

    g.secrets = get_secrets()

#This gets executed by default by the browser if no page is specified
#So.. we redirect to the endpoint we want to load the base page
@app.route('/welcome') #endpoint
def index():
    return send_from_directory('static','welcome.html')


@app.route("/secure_api/<proc_name>",methods=['GET', 'POST'])
@token_required
def exec_secure_proc(proc_name):
    logger.debug(f"Secure Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('secure_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
        app.logger.info('In the try')
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        app.logger.info('Instant error')
        return json_response(status_=409 ,data=ERROR_MSG)

    return resp



@app.route("/open_api/<proc_name>",methods=['GET', 'POST'])
def exec_proc(proc_name):
    logger.debug(f"Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('open_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp

#Returns list of books given jwt
@app.route('/books')
def getBooks():

    token = request.headers.get('JWT')

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE token = %s;").format(sql.Identifier('users')),(token,))
    userInfo = db.fetchone()
    db.close()

    if(userInfo == None):
        return("Invalid Token")



    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM books"))
    currentBooks = db.fetchall()



    if(currentBooks == None):
        return("The store currently does not have books")

    books = []

    for book in currentBooks:
        books.append({"ISBN": book[0], "Title": book[1], "Author": book[2], "Price": book[3] + " USD"})

    return jsonify(books)








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
