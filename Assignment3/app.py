from flask import Flask,render_template,request, send_from_directory
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import datetime
import bcrypt

from psycopg2 import sql
from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images",
            "SAN" : "https://media2.giphy.com/media/kfozgIgxf5qyvWwByh/giphy.gif"
            }

CUR_ENV = "PRD"
JWT_SECRET = None

global_db_con = get_db()

with open("secret", "r") as f:
    JWT_SECRET = f.read()


#Welcome Base Page
@app.route('/welcome')
def welcome():
    return send_from_directory('static','welcome.html')



# Creates User Account
@app.route('/create', methods=['POST'])
def createAccount():
    data = request.get_json()
    username = data['username']
    password = data['password']

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM users WHERE username = %s;"),(username,))
    userPass = db.fetchone()

    if userPass != None:
        db.close()

        if userPass[2] == password:
            return(f"Account already active. JWT token = {userPass[0]}")

        return(f"An account with {username} is already taken")

    token = jwt.encode(
            {
                'username': username, 
                'password': password 
            }, JWT_SECRET, algorithm="HS256")

    db.execute(sql.SQL("INSERT INTO users (token, username, password) VALUES (%s, %s, %s);"), (token, username,password))
    db.close()

    global_db_con.commit()

    return(f"Successfully created account. Username = {username} and token = {token}")




#Returns list of books given jwt
@app.route('/books')
def getBooks():
    return("books")


app.run(host='0.0.0.0', port=80)

