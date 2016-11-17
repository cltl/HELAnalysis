var express = require('express');
var app = express();

app.get('/', function(req, res){
    res.sendFile('index.html', {root:'./client'});
});

app.use('/', express.static('client/'));

app.listen(8282, function() {
	console.log('started analyzer nodejs backend');
});
