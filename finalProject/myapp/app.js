const express = require('express');
const swaggerJSDoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const app = express();
const port = 3000

var auth = require('./routes/auth.js')
var movie = require('./routes/movie.js')
var addmovie = require('./routes/addMovie.js')
var deletemovie = require('./routes/deleteMovie.js')


app.use(express.json());


const swaggerDefinition = {
  openapi: '3.0.0',
  info: {
    title: 'Movie API Documentation',
    version: '1.0.0',
    description:
      'This is a simple REST API application made using Express',
    contact: {
      name: 'CS444 Final Project API',
      url: 'https://github.com/joshhMD',
    },
  },
  servers: [
    {
      url: 'http://localhost:3000',
      description: 'Dev server',
    },
  ],
};

const options = {
  swaggerDefinition,
  // Paths to files containing OpenAPI definitions
  apis: ['myapp/routes/*.js'],
};

const swaggerSpec = swaggerJSDoc(options);




app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
app.use('/auth', auth)
app.use('/movie', movie)
app.use('/addMovie', addmovie)
app.use('/deleteMovie', deletemovie)

app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`)
})