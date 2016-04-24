RingCentral 3-Legged OAuth Demo in Python
=========================================

## Overview

This is a quick 3-legged OAuth demo that runs using Python 2.7 and Bottle.

## Installation

```bash
$ pip install bottle
$ pip install requests
$ pip install python-dotenv
$ pip install ringcentral
```

## Configuration

Edit the `.env` file to add your application key and application secret.

```bash
$ cd ringcentral-oauth-demos/python-bottle
$ cp config-sample.env.txt .env
$ vi .env
```

## Usage

Open the web page:

```bash
$ python app.py
```

Go to the URL:

```
http://localhost:4567
````

Then click the <input type="button" value="Login with RingCentral"> button to authorize the demo app and view the access token.
