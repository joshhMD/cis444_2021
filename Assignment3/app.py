from flask import Flask,render_template,request
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

#Make user account and return jwt
@app.route('/auth')
def authenticate():
    return("return jwt")

#Returns list of books given jwt
@app.route('/books')
def getBooks():
    return("books")


#Welcome Base Page
@app.route('/')
def welcome():
    return render_template('welcome.html')


app.run(host='0.0.0.0', port=80)

