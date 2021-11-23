from flask import g,Flask,render_template,jsonify,request,send_from_directory
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

import jwt

import datetime
import bcrypt
from psycopg2 import sql
from db_con import get_db_instance, get_db



global_db_con = get_db()


def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user

    username = request.form['username']

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE username = %s").format(sql.Identifier('users')),(username,))
    userPass = db.fetchone()
    db.close()

    if userPass == None:
        return json_response(data = 'Invalid credentials')






    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE username = %s;").format(sql.Identifier('purchases')),(username,))
    historyDB = db.fetchall()
    db.close() 
    


    purchaseHistory = []


    for purchase in historyDB:
        purchaseHistory.append({"Username": purchase[0], "Title": purchase[1], "Price": purchase[2],"Date": purchase[3]})

    return json_response(data = purchaseHistory)
