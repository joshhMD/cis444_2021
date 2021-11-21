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

    username = request.form['username']
    password = request.form['password']
    
    #data = request.get_json()
    #username = data['username']
    #password = data['password']

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE username = %s;").format(sql.Identifier('users')),(username,))
    userPass = db.fetchone()
    db.close()

    if userPass != None:

        tempPass = bytes(userPass[2], 'utf-8')
        if bcrypt.checkpw(bytes(password, 'utf-8'), tempPass):
            return(f"Account active. JWT token = {userPass[0]}")

        return("Invalid Credentials: Password")

    return("Invalid Credentials: Username")
