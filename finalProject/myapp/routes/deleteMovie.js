const express = require('express')
const router= express.Router()

var jwt = require('jsonwebtoken');
var Promise = require('promise');
var mongojs = require('mongojs');
var db = mongojs('finaldatabase', ['finaldatabase'])



/**
 * @swagger
 * /deleteMovie:
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
 *                 Response:
 *                   type: string
 *                   description: The request response
 *                   example: Success
 *                 Result:
 *                   type: string
 *                   description: The movie's director
 *                   example: Removed Avatar
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
 *                   description: The error response
 *                   example: Invalid movie title
*/
router.post('/', function (req, res) {

    if(req.headers['token'])
    {
        var token = req.headers['token']
    }
    else
    {
        res.send({"Response": "Fail",
                  "Error": "Enter token"})
    }

    if(!req.body.title)
    {
        res.send({"Response": "Fail",
                  "Error": "Missing movie title"})
    }

    var promiseArray = [];
    
    promiseArray.push(checkUser(token));

    Promise.all(promiseArray).then(allValues => {

        var moviePromise = [];
        moviePromise.push(removeMovie(req.body.title));

        Promise.all(moviePromise).then(allResults => {
            console.log(allResults)
            res.send({"Response": "Success",
                      "Result": "Removed: " + req.body.title})

        }).catch(errMovie => {
            if(errMovie == false)
            {
                console.log("Movie not in database");
                res.send({"Response": "Fail",
                          "Error": "Movie not in database"})
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

function removeMovie(title)
{
    return new Promise(function (resolve, reject) {
        db.collection("Movies").findOne({"title":title},function(err, movie) 
        {
            if(err)
            {
                return reject(err);
            }
            else if(movie)
            {
                db.Movies.remove(movie, function(insertErr, movieResult) 
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