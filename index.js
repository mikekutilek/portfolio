//index.js

const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const http = require('http');
const csv = require('csvtojson');

//Constants
const PORT = process.env.OPENSHIFT_NODEJS_PORT || 8080;
const HOST = '172.30.144.77' || 'http://portfolio-mikekutilek-portfolio.a3c1.starter-us-west-1.openshiftapps.com' || '127.0.0.1'
var client_id = '23b9b00767a84fa7aecfdd41a118d2df';
var client_secret = '7651a04c818b469ab40c9782e962be68';
var redirect_uri = 'http://localhost:' + PORT;
var scopes = 'user-read-private user-read-email';



//App
const app = express();



app.listen(PORT, HOST, () => {
    console.log(`Running on http://${HOST}:${PORT}`);
});

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

app.get('/pitch-type', (req, res) => {
    res.sendFile("professional/pitch-type.html", {root: __dirname });
});

app.get('/matchup', (req, res) => {
	res.sendFile("professional/projects/matchup_tool.html", {root: __dirname });
});

app.get('/galleries', (req, res) => {
	res.sendFile("config/galleries.json", {root: __dirname });
});



function call_pitchtype(req, res){
    var pid = req.params.pid;
    var spawn = require("child_process").spawn;
    var process = spawn('python', ["./pitch_type.py", pid]);

    process.stdout.on('data', function (data){
        res.send(data.toString());
        res.end();
    })
};

function call_pitchers(req, res){
    //res.send("hi");
    //var pid = req.params.pid;
    
    var spawn = require("child_process").spawn;
    var process = spawn('python', ["./get_std_data.py"]);
    process.stdout.on('data', function (data){
        res.send(data.toString());
        res.end();
    })
};

app.get('/api/v1/fangraphs/pitching', call_pitchers);

app.get('/api/v1/fangraphs/pitching/pitch-type/:pid', call_pitchtype);

