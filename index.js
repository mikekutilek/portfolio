//index.js

const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const bodyParser = require('body-parser');
const path = require('path');


//Constants
const PORT = 8080;
const HOST = 'localhost';

//App
const app = express();

app.use(express.static(__dirname + '/'));

app.get('/', (req, res) => {
	res.sendFile("index.html", {root: __dirname });
});

app.get('/photography', (req, res) => {
	res.sendFile("photography.html", {root: __dirname });
});

app.get('/videography', (req, res) => {
	res.sendFile("videography.html", {root: __dirname });
});

app.get('/galleries', (req, res) => {
	res.sendFile("config/galleries.json", {root: __dirname });
});

app.listen(PORT, HOST, () => {
	console.log(`Running on http://${HOST}:${PORT}`);
});