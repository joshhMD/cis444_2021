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
    token = request.form['jwt']
    title = request.form['title']

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE token = %s;").format(sql.Identifier('users')),(token,))
    userInfo = db.fetchone()
    db.close()

    if(userInfo == None):
        return json_response(data = "Invalid Token")



    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM {} WHERE title = %s;").format(sql.Identifier('purchases')),(title,))
    tempCheck = db.fetchone()
    db.close()

    if tempCheck == None:
        return json_response(data = "You do not own this!")


    db = global_db_con.cursor()
    db.execute(sql.SQL("DELETE FROM {} WHERE title = %s").format(sql.Identifier('purchases')), (title,))
    db.close()

    global_db_con.commit()

    return json_response(data = "Successfully sold!")
