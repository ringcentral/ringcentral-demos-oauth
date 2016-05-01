require('dotenv').config();
var https = require('https');
var app = require('express')();

var ringcentral = require('ringcentral');

// Configure Mustache
var mustacheExpress = require('mustache-express');
app.engine('mustache', mustacheExpress());
app.set('view engine', 'mustache');
app.set('views', __dirname + '/views');

var useTls = process.env.MY_APP_TLS_ENABLED > 0 ? true : false;
var server = null;

var port = process.env.MY_APP_PORT;

if (useTls) {
  var tls = require('tls'),
      fs = require('fs');
  server = https.createServer({
    key: fs.readFileSync(process.env.MY_APP_TLS_PRIVATE_KEY),
    cert: fs.readFileSync(process.env.MY_APP_TLS_PUBLIC_CERT)
  }, app).listen(port, function() {
    console.log('LISTEN_HTTPS ' + port);    
  });
} else if (! useTls) {
  server = require('http').Server(app);
  server.listen(port, function() {
    console.log('LISTEN_HTTP ' + port);    
  });
}

var rcsdk = new ringcentral({
  server: process.env.RC_APP_SERVER_URL,
  appKey: process.env.RC_APP_KEY,
  appSecret: process.env.RC_APP_SECRET
});

app.get('/', function(req, res) {
  // Get token for display after OAuth
  token = rcsdk.platform().auth().data();
  token_json = token['access_token'] ? JSON.stringify(token, null, ' ') : '';

  // Render home page with params
  res.render('index', {
    authorize_uri: rcsdk.platform().authUrl({
      redirectUri: process.env.RC_APP_REDIRECT_URL
    }),
    redirect_uri: process.env.RC_APP_REDIRECT_URL,
    token_json: token_json
  });
});

app.get('/callback', function(req, res) {
  if (req.query.code) {
    rcsdk.platform()
      .login({
        code: req.query.code,
        redirectUri: process.env.RC_APP_REDIRECT_URL
      })
      .then(function(response) {
        console.log('logged_in');
        res.send('');
      })
      .catch(function(e) {
        console.log('ERR ' + e.message  || 'Server cannot authorize user');
        res.send('');
      });
  }
});
