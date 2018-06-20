//index.js

const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const http = require('http');

//Constants
const PORT = 8080;
const HOST = 'localhost';
var client_id = '23b9b00767a84fa7aecfdd41a118d2df';
var client_secret = '7651a04c818b469ab40c9782e962be68';
var redirect_uri = 'http://localhost:' + PORT;
var scopes = 'user-read-private user-read-email';

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

http.createServer(function(request, response){
	response.writeHead(200, {"Content-Type": "text/plain"});
	response.write("Hello World");
	response.end();
})

app.listen(PORT, HOST, () => {
	console.log(`Running on http://${HOST}:${PORT}`);
});