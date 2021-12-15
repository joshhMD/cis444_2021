const express = require('express')
const router= express.Router()

var jwt = require('jsonwebtoken');
var Promise = require('promise');
var mongojs = require('mongojs');
var db = mongojs('finaldatabase', ['finaldatabase'])

/**
 * @swagger
 * /auth:
 *   post:
 *     summary: Authenticates a user and generates a token
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               username:
 *                 type: string
 *                 description: The username
 *                 example: Josh123
 *               password:
 *                 type: string
 *                 description: The password
 *                 example: password123
 *     responses:
 *       200:
 *         description: Successful authentication with returned API token
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 Response:
 *                   type: string
 *                   description: The outcome of the request
 *                   example: Success
 *                 name:
 *                   type: string
 *                   description: The user's token
 *                   example: f4uhf734bfu934hf934b9f349fn4nfjndfjn38fn
 *       400:
 *         description: Failed authentication of user
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 Response:
 *                   type: string
 *                   description: The outcome of the request
 *                   example: Fail
 *                 Error:
 *                   type: string
 *                   description: The Error Response
 *                   example: Account already exists
*/
router.post('/', function (req, res) {

    if(req.body.username && req.body.password)
    {
        var username = req.body.username
        var password = req.body.password
    }
    else
    {
        res.send("NOT ENOUGH INFO")
        res.send({"Response": "Fail",
                  "Error": "Missing body arguments"})
    }

    var promiseArray = [];
    
    promiseArray.push(createUser(username, password));

    Promise.all(promiseArray).then(allValues => {
            console.log("Account Successfully created. Token is: " + allValues[0])
            res.send({"Response": "Success",
                      "Token": allValues[0]})
    }).catch(err => {
        if(err == false)
        {
            console.log("ERRORR ACCOUNT ALREADY EXISTS");
            res.send({"Response": "Fail",
                      "Error": "Account already exists"})
        }
        else
        {
            console.log(err);
            res.status(400).send(err);
        }
    });
    
})


function createUser(username, password)
{
    return new Promise(function (resolve, reject) {
        db.collection("Users").findOne({'username': username, 'password': password}, function(err, returnedRecord) 
        {
            if(err)
            {
                return reject(err);
            }
            else if(!returnedRecord)
            {
                var token = jwt.sign({ user: username, pass: password }, 'shhhhh');

                var record = {
                    "username": username,
                    "password": password,
                    "token": token
                }

                
                db.Users.insert(record, function(insertErr, tokenResult) 
                {
                    if(insertErr)
                    {
                        return reject(insertErr)
                    }
                    else
                    {
                        return resolve(token);
                    }
                });
            }
            else
            {
                return reject(false);
            }
        });
    });
}

module.exports = router;