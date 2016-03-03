var Express = require('express');
var path = require('path');
var fs = require('fs');
var Promise = require('bluebird');
var moment = require('moment');
fs.readFile = Promise.promisify(fs.readFile);
var CombinedStream = require('combined-stream');
var JSONStream = require('JSONStream');
var EventEmitter = require('events').EventEmitter;
var app = Express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'rss'));

app.get('/', function(req, res){
    var nowDate = moment();
    var allData = [];
    var appendMonthes = req.query.appendmonthes || 0;
    appendMonthes = appendMonthes > 12 ? 12 : appendMonthes;
    var parser = JSONStream.parse('*');
    var combinedStream = CombinedStream.create();
    combinedStream.append(fs.createReadStream(path.join(__dirname, 'rss', nowDate.format("YYYYMM") + '.json')));
    
    while(appendMonthes > 0){
        nowDate = nowDate.subtract(1, 'months');
        console.log("Concating", path.join(__dirname, 'rss', nowDate.format("YYYYMM") + '.json'))
        combinedStream.append(fs.createReadStream(path.join(__dirname, 'rss', nowDate.format("YYYYMM") + '.json')));
        appendMonthes--;
    }
    
    parser.on('data', function(data){
        data.pubDate = moment(data.publish_date, 'YYYY/MM/DD').format();
        allData.push(data);
    })
    
    parser.on('end', function() {
        console.log(allData);
        res.render('item', {items: allData, nowTime: moment().format()});
    })
    
    combinedStream.pipe(parser);
});

app.get('/date/:date', function(req, res){
    var date = req.params.date;
    var allData = [];
    
    fs.readFile(path.join(__dirname, 'rss', date+'.json'))
    .then(function(data){
        allData = JSON.parse(data);
        allData.forEach(function(data){
            data.pubDate = moment(data.publish_date, 'YYYY/MM/DD').format();
        })
        res.render('item', {items: allData, nowTime: moment().format()});
    })
    .catch(function(err){
        console.error(err);
    });
})

app.listen(3081, function(){
    console.log("Server started at port 3081");
})
