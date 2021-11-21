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
    logger.debug("Login Handle Request")


    userN = request.form['username']


    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE username = %s;").format(sql.Identifier('purchases')),(userN,))
    historyDB = db.fetchall()
    db.close() 
    


    purchaseHistory = []


    for purchase in historyDB:
        purchaseHistory.append({"Username": purchase[0], "Title": purchase[1], "Price": purchase[2],"Date": purchase[3]})

    return jsonify(purchaseHistory)
