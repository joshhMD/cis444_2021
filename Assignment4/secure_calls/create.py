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

    if userPass != None:
        db.close()
        
        tempPass = bytes(userPass[2], 'utf-8')
        if bcrypt.checkpw(bytes(password, 'utf-8'), tempPass):
            return(f"Account already active. JWT token = {userPass[0]}")

        return(f"An account with {username} is already taken")

    salted = bcrypt.hashpw( bytes(password,  'utf-8' ) , bcrypt.gensalt(10))
    decryptSalt = salted.decode('utf-8')
    password = decryptSalt


    token = jwt.encode(
            {
                'username': username,
                'password': password
            }, JWT_SECRET, algorithm="HS256")

    db.execute(sql.SQL("INSERT INTO {} (token, username, password) VALUES (%s, %s, %s);").format(sql.Identifier('users')), (token, username,password))
    db.close()

    global_db_con.commit()

    return(f"Successfully created account. Username = {username} and token = {token}")
