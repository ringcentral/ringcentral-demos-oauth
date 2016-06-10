RingCentral 3-Legged OAuth Demo in JavaScript with PHP
==========================================================

## Overview

This is a quick 3-legged OAuth demo that runs using PHP.

## Installation

### Via NPM

```bash
$ git clone https://github.com/grokify/ringcentral-demos-oauth
$ cd ringcentral-demos-oauth/php
$ composer install
```

## Configuration

Edit the `.env` file to add your application key and application secret.

```bash
$ cd ringcentral-demos-oauth/php
$ cp .env.sample .env
$ vi .env
```

In the [Developer Portal](http://developer.ringcentral.com/), ensure the redirect URI in your config file has been entered in your app configuration. By default, the URL is set to the following for this demo:

```
http://localhost:8080/callback.php
```

## Usage

Open the web page:

```bash
$ php -S localhost:8080
```

Go to the URL:

```
http://localhost:8080
````

Then click the <input type="button" value="Login with RingCentral"> button to authorize the demo app and view the access token.
