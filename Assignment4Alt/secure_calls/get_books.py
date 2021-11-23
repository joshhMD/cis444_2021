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
    logger.debug("Get Books Handle Request")
    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM books"))
    currentBooks = db.fetchall()

    books1 = []

    for book in currentBooks:
        books1.append({"ISBN": book[0], "Title": book[1], "Author": book[2], "Price": book[3] + " USD"})

    return json_response( token = create_token(  g.jwt_data ) , books = books1)
