//index.js

const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const http = require('http');
const csv = require('csvtojson');

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
	res.sendFile("personal/photography.html", {root: __dirname });
});

app.get('/videography', (req, res) => {
	res.sendFile("personal/videography.html", {root: __dirname });
});

app.get('/time-lapse', (req, res) => {
	res.sendFile("personal/time-lapse.html", {root: __dirname });
});

app.get('/projects', (req, res) => {
	res.sendFile("professional/projects.html", {root: __dirname });
});

app.get('/matchup', (req, res) => {
	res.sendFile("professional/projects/matchup_tool.html", {root: __dirname });
});

app.get('/galleries', (req, res) => {
	res.sendFile("config/galleries.json", {root: __dirname });
});

app.get('/api/v1/fangraphs/pitching/pitch-type', call_pitchtype);

function call_pitchtype(req, res){
    var spawn = require("child_process").spawn;
    var process = spawn('python', ["./pitch_type.py"]);

    process.stdout.on('data', function (data){
        res.send(data.toString());
    })
}



app.get('/api/v1/fangraphs/batting/standard/', (req, res) => {
	var options = {
        delimiter : ',',
        quote : '"'
    };
    var filename = "c:/Users/makut/Documents/Data/Fangraphs/Batting/2018/Standard Batting Data.csv";
    //var team = req.params.team;
    var contents = fs.readFileSync(filename);
    csv()
    .fromFile(filename)
    .then((jsonObj) => {
    	return new Promise((resolve, reject)=> {
    		res.send(jsonObj.length);
    	})
    	
    })
});



http.createServer(function(request, response){
	response.writeHead(200, {"Content-Type": "text/plain"});
	response.write("Hello World");
	response.end();
})

app.listen(PORT, HOST, () => {
	console.log(`Running on http://${HOST}:${PORT}`);
});