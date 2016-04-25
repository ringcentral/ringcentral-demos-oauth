RingCentral 3-Legged OAuth Demo in Python
=========================================

## Overview

This is a quick 3-legged OAuth demo that runs using Python 2.7 and Bottle with the [RingCentral Python SDK](https://github.com/ringcentral/ringcentral-python) v0.6.1.

## Installation

```bash
$ pip install bottle
$ pip install python-dotenv
$ pip install requests
$ pip install ringcentral
```

## Configuration

Edit the `.env` file to add your application key and application secret.

```bash
$ cd ringcentral-oauth-demos/python-bottle
$ cp config-sample.env.txt .env
$ vi .env
```

In the [Developer Portal](http://developer.ringcentral.com/), ensure the redirect URI in your config file has been entered in your app configuration. By default, the URL is set to the following for this demo:

```
http://localhost:8080/callback
```

## Usage

Open the web page:

```bash
$ python app.py
```

Go to the URL:

```
http://localhost:8080
````

Then click the <input type="button" value="Login with RingCentral"> button to authorize the demo app and view the access token.
