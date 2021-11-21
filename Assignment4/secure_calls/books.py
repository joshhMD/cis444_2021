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
