var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017";

var app, express;

//establish a server
express = require("express");

app = express();
var bodyParser = require('body-parser');
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

// 为了和angular连用，这里要设置允许跨域访问
var allowCrossDomain = function (req, res, next) {
    res.header('Access-Control-Allow-Origin', 'http://localhost:4200');
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type,Authorization');
    res.header('Access-Control-Allow-Credentials', 'true');
    next();
};
app.use(allowCrossDomain);


const dbName = 'mk';
const collectionName = "d2018_03_24";
//1. The front end want to get all products information.
app.get("/products", function (req, res) {
    // console.log("get your request")
    MongoClient.connect(url, function(err, client) {
        if (err) throw err;
        db = client.db(dbName);
        db.collection(collectionName).find({}).toArray( function(err, result) {
            // console.log(result)
            if (err) throw err;
            res.send(result);
        });
    });
});




//start to listen port 8888
app.listen(8888);
