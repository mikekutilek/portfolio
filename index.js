//index.js

const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const http = require('http');
const csv = require('csvtojson');

setInterval(function() {
    http.get("http://mikekutilek.herokuapp.com");
}, 300000); // every 5 minutes (300000)

//Constants
const PORT = process.env.PORT || process.env.OPENSHIFT_NODEJS_PORT || 8080;
//const HOST = process.env.IP || process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1' || '0.0.0.0'
var client_id = '23b9b00767a84fa7aecfdd41a118d2df';
var client_secret = '7651a04c818b469ab40c9782e962be68';
//var redirect_uri = 'http://localhost:' + PORT;
var scopes = 'user-read-private user-read-email';

const uri = "mongodb+srv://admin:pdometer@mongo-uwij2.mongodb.net/test?retryWrites=true";

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

app.get('/war-model', (req, res) => {
    res.sendFile("html/war-model.html", {root: __dirname });
});

app.get('/war-ranks-hist', (req, res) => {
    res.sendFile("projects/SABR/graphs/war_ranks_hist.html", {root: __dirname });
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
    if (team == "ANY"){
        var team_array = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CIN', 'CLE', 'COL', 'CWS', 'DET', 'HOU', 'KC', 'LAA', 'LAD', 'MIA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SD', 'SEA', 'SF', 'STL', 'TB', 'TEX', 'TOR', 'WSH'];
    }
    else {
        var team_array = [team];
    }
    var pos = req.params.pos;
    var hand = req.params.hand;

    const client = new MongoClient(uri, { useNewUrlParser: true });
    client.connect(err => {
        var dbo = client.db("SABR");
        dbo.collection('opener_candidates').find( { $and: [ { Pos : pos }, { Team : {$in : team_array} }, { Hand : hand } ] } ).sort({ wOBA : -1 }).toArray(function(err, result){
            if (err) {
                console.log(err);
            }
            res.send(result);
        });
        
    });
    client.close();
};

function call_chunk(req, res){
    var team = req.params.team;
    const client = new MongoClient(uri, { useNewUrlParser: true });
    client.connect(err => {
        var dbo = client.db("SABR");
        dbo.collection('bref_team_sp').find({Tm : {'$ne':'LgAvg'}}).sort({ ['RA/G'] : 1 }).toArray(function(err, result){
            if (err) {
                console.log(err);
            }
            var elite = result.slice(0, 6);
            var good = result.slice(6, 12);
            var average = result.slice(12, 18);
            var bad = result.slice(18, 24);
            var terrible = result.slice(24, 30);
            var chunk = "";
            if (elite.some(e => e.Tm === team)){
                chunk = " have a starting rotation in the upper echelon of MLB in RA/G. They probably don't need an opener, but you can still take a look at potential options.";
            }
            else if (good.some(e => e.Tm === team)){
                chunk = " have a starting rotation in one of the higher tiers of MLB in RA/G. They may or may not need an opener to fill a void, but you can still take a look at potential options.";
            }
            else if (average.some(e => e.Tm === team)){
                chunk = " have a starting rotation in the middle of MLB in RA/G. They might need an opener to fill a void. Check out their options below!";
            }
            else if (bad.some(e => e.Tm === team)){
                chunk = " have a starting rotation in one of the lower tiers of MLB in RA/G. They could probably use an opener to fill a void. See options below!";
            }
            else if (terrible.some(e => e.Tm === team)){
                chunk = " have a starting rotation at the very bottom of MLB in RA/G. They definitely have a rotation spot that could be better utilized. See options below!";
            }
            else {
                chunk = " team was not found";
            }
            res.send(chunk);
        });
        
    });
    client.close();
};

function call_nhl_fp(req, res){
    var table = req.params.table;
    var sort = req.params.sort;
    const client = new MongoClient(uri, { useNewUrlParser: true });
    client.connect(err => {
        var dbo = client.db("Corsica");
        dbo.collection(table).find().sort({ [sort] : -1 }).toArray(function(err, result){
            if (err) {
                console.log(err);
            }
            res.send(result);
        });
        
    });
    client.close();
};

function call_nfl_fp(req, res){
    var pos = req.params.pos;
    if (pos.toUpperCase() == 'FLEX'){
        pos_array = ['RB', 'WR', 'TE'];
    }
    else{
        pos_array = [pos];
    }
    var sort = req.params.sort;
    const client = new MongoClient(uri, { useNewUrlParser: true });
    client.connect(err => {
        var dbo = client.db("WOPR");
        dbo.collection('fp').find({ Pos : { $in: pos_array }}).sort({ [sort] : -1 }).toArray(function(err, result){
            if (err) {
                console.log(err);
            }
            res.send(result);
        });
        
    });
    client.close();

};

function call_mlb_fp(req, res){
    var table = req.params.table;
    var sort = req.params.sort;
    const client = new MongoClient(uri, { useNewUrlParser: true });
    client.connect(err => {
        var dbo = client.db("SABR");
        dbo.collection(table).find().sort({ [sort] : -1 }).toArray(function(err, result){
            if (err) {
                console.log(err);
            }
            res.send(result);
        });
        
    });
    client.close();
};

function get_mlb_teams(req, res){
    const client = new MongoClient(uri, { useNewUrlParser: true });
    client.connect(err => {
        var dbo = client.db("SABR");
        dbo.collection('teams').find().sort({ ['master_abbr'] : 1 }).toArray(function(err, result){
            if (err) {
                console.log(err);
            }
            res.send(result);
        });
        
    });
    client.close();
};

app.get('/api/v1/sabr/teams', get_mlb_teams);

app.get('/api/v1/sabr/opener/:team/:pos/:hand', call_candidates);

app.get('/api/v1/sabr/opener/:team', call_chunk);

app.get('/api/v1/fangraphs/pitching', call_pitchers);

app.get('/api/v1/fangraphs/pitching/pitch-type/:pid', call_pitchtype);

app.get('/api/v1/corsica/:table/:sort', call_nhl_fp);

app.get('/api/v1/wopr/fp/:pos/:sort', call_nfl_fp);

app.get('/api/v1/sabr/:table/:sort', call_mlb_fp);