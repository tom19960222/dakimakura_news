var Express = require('express');
var serveStatic = require('serve-static')
var path = require('path');
var app = Express();

var options = {
  dotfiles: 'ignore',
  etag: false,
  extensions: ['xml'],
  index: false,
  maxAge: '1d',
  redirect: false,
}

app.use(serveStatic(path.join(__dirname, 'rss'), options));

app.get('/', function(req, res){
    var nowDate = new Date();
    var filename = path.join(__dirname, 'rss', nowDate.getFullYear() + ("0" + (nowDate.getMonth()+1)).slice(-2) + '.xml');
    res.sendFile(filename, function(err){
        res.status(500).send(err);
    });
});

app.listen(3081, function(){
    console.log("Server started at port 3081");
})
