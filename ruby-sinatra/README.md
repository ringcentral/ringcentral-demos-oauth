RingCentral 3-Legged OAuth Demo in Ruby
=======================================

## Overview

This is a quick 3-legged OAuth demo that runs using Ruby and Sinatra.

## Installation

### Via Bundler

```bash
$ git clone https://github.com/grokify/ringcentral-oauth-demos
$ cd ringcentral-oauth-demos/ruby-sinatra
$ bundle
```

### Via Ruby Gems

```bash
$ gem install ringcentral_sdk
$ gem install sinatra
$ git clone https://github.com/grokify/ringcentral-oauth-demos
```

## Configuration

Edit the `.env` file to add your application key and application secret.

```bash
$ cd ringcentral-oauth-demos/ruby-sinatra
$ cp config-sample.env.txt .env
$ vi .env
```

## Usage

Open the web page:

```bash
$ ruby app.rb
```

Then click the <input type="button" value="Login with RingCentral"> button to authorize the demo app and view the access token.
