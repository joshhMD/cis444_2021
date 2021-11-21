from flask import request,g,Flask,render_template,jsonify,send_from_directory
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

import jwt
import datetime
import bcrypt

from psycopg2 import sql
from db_con import get_db_instance, get_db

from tools.logging import logger

global_db_con = get_db()



def handle_request():
    logger.debug("Login Handle Request PURCHASEE")


    userN = request.form['username']
    #token = request.form['jwt']
    token = request.form['jwt']
    title = request.form['title']

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE token = %s;").format(sql.Identifier('users')),(token,))
    userInfo = db.fetchone()
    db.close()

    if(userInfo == None):
        return json_response(data = "Invalid user")



    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE title = %s;").format(sql.Identifier('books')),(title,))
    buy = db.fetchone()
    db.close()

    if buy == None:
        return json_response(data = "Invalid Book")

    price = buy[3]
    buyDate = datetime.datetime.now()


    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE title = %s;").format(sql.Identifier('purchases')),(title,))
    tempCheck = db.fetchone()
    db.close()

    if tempCheck != None:
        return json_response(data = "Already own this")


    db = global_db_con.cursor()
    db.execute(sql.SQL("INSERT INTO {} (username, title, price, date) VALUES (%s, %s, %s, %s);").format(sql.Identifier('purchases')), (userN, title, price, buyDate))
    db.close()

    global_db_con.commit()

    return json_response(data = "Successfully purchased!")
