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
    logger.debug("Buyy Book Handle Request")

    userN = request.form['username']
    title = request.form['title']
    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE title = %s;").format(sql.Identifier('books')),(title,))
    buy = db.fetchone()
    db.close()

    if buy == None:
        return json_response(token = create_token(  g.jwt_data ) ,data = "Invalid Book")

    price = buy[3]
    buyDate = datetime.datetime.now()


    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE title = %s;").format(sql.Identifier('purchases')),(title,))
    tempCheck = db.fetchone()
    db.close()

    if tempCheck != None:
        return json_response(token = create_token(  g.jwt_data ) ,data = "Already own this")


    db = global_db_con.cursor()
    db.execute(sql.SQL("INSERT INTO {} (username, title, price, date) VALUES (%s, %s, %s, %s);").format(sql.Identifier('purchases')), (userN, title, price, buyDate))
    db.close()    

    global_db_con.commit()



    return json_response( token = create_token(  g.jwt_data ) , data = "Successfully purchased")
