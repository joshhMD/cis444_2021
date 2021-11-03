from flask import Flask,render_template,jsonify,request,send_from_directory
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


# Registers a User
@app.route('/register', methods=['POST'])
def registerAccount():
    username = request.form['username']
    password = request.form['password']

    #data = request.get_json()
    #username = data['username']
    #password = data['password']

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM users WHERE username = %s;"),(username,))
    userPass = db.fetchone()

    if userPass != None:
        db.close()

        return("false")
    
    salted = bcrypt.hashpw( bytes(password,  'utf-8' ) , bcrypt.gensalt(10))
    decryptSalt = salted.decode('utf-8')
    password = decryptSalt


    token = jwt.encode(
            {
                'username': username,
                'password': password
            }, JWT_SECRET, algorithm="HS256")

    db.execute(sql.SQL("INSERT INTO users (token, username, password) VALUES (%s, %s, %s);"), (token, username,password))
    db.close()

    global_db_con.commit()

    return("true")






# Creates User Account
@app.route('/create', methods=['POST'])
def createAccount():
    username = request.form['username']
    password = request.form['password']
    
    #data = request.get_json()
    #username = data['username']
    #password = data['password']

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM users WHERE username = %s;"),(username,))
    userPass = db.fetchone()

    if userPass != None:
        db.close()

        if userPass[2] == password:
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

    db.execute(sql.SQL("INSERT INTO users (token, username, password) VALUES (%s, %s, %s);"), (token, username,password))
    db.close()

    global_db_con.commit()

    return(f"Successfully created account. Username = {username} and token = {token}")


# Authenticates a User and returns jwt
@app.route('/auth', methods=['POST'])
def authAccount():
    username = request.form['username']
    password = request.form['password']
    
    #data = request.get_json()
    #username = data['username']
    #password = data['password']

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM users WHERE username = %s;"),(username,))
    userPass = db.fetchone()
    db.close()

    if userPass != None:

        tempPass = bytes(userPass[2], 'utf-8')
        if bcrypt.checkpw(bytes(password, 'utf-8'), tempPass):
            return(f"Account active. JWT token = {userPass[0]}")

        return("Invalid Credentials: Password")

    return("Invalid Credentials: Username")






#Checks if credentials are correct
@app.route('/login', methods=['POST'])
def login():
    #data = request.get_json()
    #username = data['username']
    

    username = request.form['username']
    password = request.form['password']

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM users WHERE username = %s"),(username,))
    userPass = db.fetchone()

    db.close()
    
    if userPass == None:
        return "false"

    else:
        tempPass = bytes(userPass[2], 'utf-8')
        if bcrypt.checkpw(bytes(password, 'utf-8'), tempPass):
            return str(userPass[0])
        else:
            return "false"


#Returns list of books given jwt
@app.route('/books')
def getBooks():

    token = request.headers.get('JWT')

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM users WHERE token = %s;"),(token,))
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


# Purchase book entry into database
@app.route('/purchase', methods=['POST'])
def purchaseBook():

    userN = request.form['username']
    token = request.form['jwt']
    title = request.form['title']

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM users WHERE token = %s;"),(token,))
    userInfo = db.fetchone()
    db.close()

    if(userInfo == None):
        return("Invalid Token") 



    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM books WHERE title = %s;"),(title,))
    buy = db.fetchone()
    db.close()

    if buy == None:
        return "false"
    
    price = buy[3]
    buyDate = datetime.datetime.now()


    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM purchases WHERE title = %s;"),(title,))
    tempCheck = db.fetchone()
    db.close()

    if tempCheck != None:
        return "You already bought this!"


    db = global_db_con.cursor()
    db.execute(sql.SQL("INSERT INTO purchases (username, title, price, date) VALUES (%s, %s, %s, %s);"), (userN, title, price, buyDate))
    db.close()

    global_db_con.commit()

    return "Successfully purchased!"


# Purchase book entry into database
@app.route('/sell', methods=['POST'])
def sellBook():

    userN = request.form['username']
    token = request.form['jwt']
    title = request.form['title']

    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM users WHERE token = %s;"),(token,))
    userInfo = db.fetchone()
    db.close()

    if(userInfo == None):
        return("Invalid Token")



    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM purchases WHERE title = %s;"),(title,))
    tempCheck = db.fetchone()
    db.close()

    if tempCheck == None:
        return "You do not own this!"


    db = global_db_con.cursor()
    db.execute(sql.SQL("DELETE FROM purchases WHERE title = %s"), (title,))
    db.close()

    global_db_con.commit()

    return "Successfully sold!"





    

# Looks up history of purchases
@app.route('/history', methods=['POST'])
def purchaseHistory():

    userN = request.form['username']


    db = global_db_con.cursor()
    db.execute(sql.SQL("SELECT * FROM purchases WHERE username = %s;"),(userN,))
    historyDB = db.fetchall()
    db.close() 
    


    purchaseHistory = []


    for purchase in historyDB:
        purchaseHistory.append({"Username": purchase[0], "Title": purchase[1], "Price": purchase[2],"Date": purchase[3]})

    return jsonify(purchaseHistory)




app.run(host='0.0.0.0', port=80)
