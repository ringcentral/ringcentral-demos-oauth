RingCentral 3-Legged OAuth Demo in JavaScript
=============================================

## Overview

This is a quick 3-legged OAuth demo that runs using client-side JavaScript with the [RingCentral JavaScript SDK](https://github.com/ringcentral/ringcentral-js) v2.0.6.

## Installation

```bash
$ cd ringcentral-demos-oauth/javascript
$ sh bower_install.sh 
```

## Configuration

Edit the `.env` file to add your application key and application secret.

```bash
$ cd ringcentral-demos-oauth/javascript/public
$ cp config-sample.js config.js
$ vi config.js
```

In the [Developer Portal](http://developer.ringcentral.com/), ensure the redirect URI in your config file has been entered in your app configuration. By default, the URL is set to the following for this demo:

```
http://localhost:8080/callback.html
```

## Usage

Open the web page:

```bash
$ npm install -g http-server
$ cd ringcentral-demos-oauth/javascript
$ http-server public
```

Go to the URL:

```
http://localhost:8080
````

Then click the <input type="button" value="Login with RingCentral"> button to authorize the demo app and view the access token.
