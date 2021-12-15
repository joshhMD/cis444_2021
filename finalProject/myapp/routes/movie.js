const express = require('express')
const router= express.Router()

var jwt = require('jsonwebtoken');
var Promise = require('promise');
var mongojs = require('mongojs');
var db = mongojs('finaldatabase', ['finaldatabase'])



/**
 * @swagger
 * /movie:
 *   get:
 *     summary: Gets movies from verified user
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
 *                   example: Invalid Movie
*/
router.get('/', function (req, res) {

    if(req.headers['token'])
    {
        var token = req.headers['token']
    }
    else
    {
        res.send({"Response": "Fail",
                  "Error": "Missing Token"})
    }

    var promiseArray = [];
    
    promiseArray.push(checkUser(token));

    Promise.all(promiseArray).then(allValues => {

        var specMovie = {};
        if(req.query.title)
        {
            specMovie["title"] = req.query.title;
        }

        var moviePromise = [];
        moviePromise.push(getMovie(specMovie));

        Promise.all(moviePromise).then(allResults => {
            console.log(allResults)
            res.send({"Response": "Success",
                      "Movies": allResults})

        }).catch(errMovie => {
            if(errMovie == false)
            {
                console.log("NO MOVIES IN DATABASE");
                res.send({"Response": "Fail",
                  "Error": "Invalid Movie"})
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

function getMovie(specMovie)
{
    return new Promise(function (resolve, reject) {
        db.collection("Movies").find(specMovie,function(err, movie) 
        {
            if(err)
            {
                return reject(err);
            }
            else if(!movie)
            {
                return reject(false)
            }
            else
            {
                return resolve(movie);
            }
        });
    });
}

module.exports = router;