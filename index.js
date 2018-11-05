//index.js

const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const http = require('http');
const csv = require('csvtojson');

//Constants
const PORT = process.env.PORT || process.env.OPENSHIFT_NODEJS_PORT || 8080;
//const HOST = process.env.IP || process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1' || '0.0.0.0'
var client_id = '23b9b00767a84fa7aecfdd41a118d2df';
var client_secret = '7651a04c818b469ab40c9782e962be68';
//var redirect_uri = 'http://localhost:' + PORT;
var scopes = 'user-read-private user-read-email';

//App
const app = express();

app.listen(PORT, () => {
    console.log(`Running on ${PORT}`);
});

app.use(express.static(__dirname + '/'));

app.get('/', (req, res) => {
	res.sendFile("index.html", {root: __dirname });
});

app.get('/photography', (req, res) => {
	res.sendFile("html/photography.html", {root: __dirname });
});

app.get('/videography', (req, res) => {
	res.sendFile("html/videography.html", {root: __dirname });
});

app.get('/about', (req, res) => {
  res.sendFile("html/about.html", {root: __dirname });
});

app.get('/projects', (req, res) => {
	res.sendFile("html/projects.html", {root: __dirname });
});

app.get('/pitch-type', (req, res) => {
    res.sendFile("html/pitch-type.html", {root: __dirname });
});

app.get('/opener', (req, res) => {
    res.sendFile("html/opener.html", {root: __dirname });
});

app.get('/fp', (req, res) => {
    res.sendFile("html/fp.html", {root: __dirname });
});

app.get('/galleries', (req, res) => {
	res.sendFile("config/galleries.json", {root: __dirname });
});

function call_pitchtype(req, res){
    var pid = req.params.pid;
    var spawn = require("child_process").spawn;
    var process = spawn('python', ["./projects/SABR/pitch_type.py", pid]);

    process.stdout.on('data', function (data){
        res.send(data.toString());
        res.end();
    })
};

function call_pitchers(req, res){
    var spawn = require("child_process").spawn;
    
    var process = spawn('python', ['./projects/SABR/get_std_data.py']);

    process.stdout.on('data', function (data){
        res.send(data.toString());
        res.end();
    })
};

function call_candidates(req, res){
    var team = req.params.team;
    var pos = req.params.pos;
    var hand = req.params.hand;
    var spawn = require("child_process").spawn;
    var process = spawn('python3', ["./projects/SABR/opener.py", team, pos, hand]);

    process.stdout.on('data', function (data){
        res.send(data.toString());
        res.end();
    })
};

function call_chunk(req, res){
    var team = req.params.team;
    var spawn = require("child_process").spawn;
    var process = spawn('python3', ["./projects/SABR/opener_chunk.py", team]);

    process.stdout.on('data', function (data){
        res.send(data.toString());
        res.end();
    })
};

function call_nhl_fp(req, res){
    var ptype = req.params.ptype;
    var spawn = require("child_process").spawn;
    var process = spawn('python3', ["./projects/Corsica/fp.py", ptype]);

    process.stdout.on('data', function (data){
        res.send(data.toString());
        res.end();
    })
};

app.get('/api/v1/corsica/fp/:ptype', call_nhl_fp);

app.get('/api/v1/fangraphs/pitching', call_pitchers);

app.get('/api/v1/fangraphs/pitching/pitch-type/:pid', call_pitchtype);

app.get('/api/v1/sabr/opener/teams', (req, res) => {
    data = {'null': 'ANY', 'Orioles': 'BAL', 'Red Sox': 'BOS', 'Yankees': 'NYY', 'Rays': 'TB', 'Blue Jays': 'TOR', 
'Indians': 'CLE', 'White Sox': 'CWS', 'Tigers': 'DET', 'Royals': 'KC', 'Twins': 'MIN',
'Astros': 'HOU', 'Angels': 'LAA', 'Athletics': 'OAK', 'Mariners': 'SEA', 'Rangers': 'TEX',
'Braves': 'ATL', 'Marlins': 'MIA', 'Mets': 'NYM', 'Phillies': 'PHI', 'Nationals': 'WSH', 
'Cubs': 'CHC', 'Reds': 'CIN', 'Brewers': 'MIL', 'Pirates': 'PIT', 'Cardinals': 'STL', 
'Diamondbacks': 'ARI', 'Rockies': 'COL', 'Dodgers': 'LAD', 'Padres': 'SD', 'Giants': 'SF'};

    res.send(data);
});

app.get('/api/v1/sabr/opener/:team/:pos/:hand', call_candidates);

app.get('/api/v1/sabr/opener/:team', call_chunk);