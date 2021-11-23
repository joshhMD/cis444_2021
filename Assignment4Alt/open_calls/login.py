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

    password = request.form['password']
    username = request.form['username']

    user = {
                    "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
           }

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE username = %s").format(sql.Identifier('users')),(username,))
    userPass = db.fetchone()
    db.close()

    if userPass == None:
        return json_response(message = 'Invalid credentials', authenticated =  False )

    else:
        tempPass = bytes(userPass[2], 'utf-8')
        if bcrypt.checkpw(bytes(password, 'utf-8'), tempPass):
            return json_response( token = create_token(user) , authenticated = True)
        else:
            return json_response(message = 'Invalid credentials', authenticated =  False )



    if not user:
        return json_response(message = 'Invalid credentials', authenticated =  False )

    return json_response( token = create_token(user) , authenticated = True)
