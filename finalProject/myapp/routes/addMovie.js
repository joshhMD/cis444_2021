const express = require('express')
const router= express.Router()

var jwt = require('jsonwebtoken');
var Promise = require('promise');
var mongojs = require('mongojs');
var db = mongojs('finaldatabase', ['finaldatabase'])



/**
 * @swagger
 * /addMovie:
 *   post:
 *     summary: Gets movies from verified user
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               title:
 *                 type: string
 *                 description: The movie title
 *                 example: The Iron Giant
 *               Director:
 *                 type: string
 *                 description: The movie director
 *                 example: Brad Bird
 *               Description:
 *                 type: string
 *                 description: The movie description
 *                 example: a giant alien robot (Vin Diesel) crash-lands near the small town of Rockwell, Maine...
 *               Budget:
 *                 type: string
 *                 description: The movie budget
 *                 example: 50 million USD
 *     parameters:
 *       - in: header
 *         name: token
 *         schema:
 *           type: string
 *         required: true
 *     responses:
 *       200:
 *         description: Successful GET of movies from backend
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 -id:
 *                   type: string
 *                   description: The record id
 *                   example: 8473847832
 *                 title:
 *                   type: string
 *                   description: The movie title
 *                   example: spider-Man
 *                 Director:
 *                   type: string
 *                   description: The movie's director
 *                   example: Sam Raimi
 *                 Description: 
 *                   type: string
 *                   description: The movie's description
 *                   example: centers on student Peter Parker (Tobey Maguire) who, after being bitten by a genetically-altered spider...
 *                 Budget:
 *                   type: string
 *                   description: The movie's budget
 *                   example: 139 million USD
 *       400:
 *         description: Failed attempt to add a movie
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
 *                   example: Movie is already in database
*/
router.post('/', function (req, res) {

    if(req.headers['token'])
    {
        var token = req.headers['token']
    }
    else
    {
        res.send({"Response": "Fail",
                  "Error": "Pleae Enter token"})
    }

    if(!req.body.title || !req.body.Director || !req.body.Description || !req.body.Budget)
    {
        res.send({"Response": "Fail",
                  "Error": "Missing body arguments"})
    }

    var promiseArray = [];
    
    promiseArray.push(checkUser(token));

    Promise.all(promiseArray).then(allValues => {

        var record = {
            "title": req.body.title,
            "Director": req.body.Director,
            "Description": req.body.Description,
            "Budget": req.body.Budget
        }

        var moviePromise = [];
        moviePromise.push(addMovie(record));

        Promise.all(moviePromise).then(allResults => {
            console.log(allResults)
            res.send({"Response": "Success",
                      "Result": allResults})
            res.send(allResults)

        }).catch(errMovie => {
            if(errMovie == false)
            {
                console.log("Movie is already in database");
                res.send({"Response": "Fail",
                          "Error": "Movie is already in database"})
            }
            else
            {
                console.log(errMovie);
                res.send(errMovie);
            }
        });
    }).catch(err => {
        if(err == false)
        {
            console.log("INVALID TOKEN");
            res.send({"Response": "Fail",
                      "Error": "Invalid Token"})
        }
        else
        {
            console.log(err);
            res.send(err);
        }
    });
    
})


function checkUser(token)
{
    return new Promise(function (resolve, reject) {
        db.collection("Users").findOne({'token': token}, function(err, returnedRecord) 
        {
            if(err)
            {
                return reject(err);
            }
            else if(!returnedRecord)
            {
                return reject(false)
            }
            else
            {
                return resolve(true);
            }
        });
    });
}

function addMovie(record)
{
    return new Promise(function (resolve, reject) {
        db.collection("Movies").findOne({"title":record['title']},function(err, movie) 
        {
            if(err)
            {
                return reject(err);
            }
            else if(!movie)
            {
                db.Movies.insert(record, function(insertErr, movieResult) 
                {
                    if(insertErr)
                    {
                        return reject(insertErr)
                    }
                    else
                    {
                        return resolve(movieResult);
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