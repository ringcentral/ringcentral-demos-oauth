RingCentral OAuth Demos
=======================

This project provides 3-legged OAuth demos for the RingCentral API in various languages using official and community SDKs.

For more information, see the [RingCentral API Developer Guide on Authorization Code Flow](https://developer.ringcentral.com/api-docs/latest/index.html#!#AuthorizationCodeFlow).

Demos are provided for:

* Client-Side Web Apps
  * [JavaScript](https://github.com/grokify/ringcentral-oauth-demos/tree/master/javascript)
* Server-Side Web Apps
  * [Python 2.7 with Bottle](https://github.com/grokify/ringcentral-oauth-demos/tree/master/python-bottle)
  * [Ruby with Sinatra](https://github.com/grokify/ringcentral-oauth-demos/tree/master/ruby-sinatra)

## Client-Side Web Apps

| Page | Description |
|------|-------------|
| Login page | This is any page with a Login button. This page will open the popup and listen for the redirect. For client-side processing, this page will also retrieve the query string parameters from the callback page. |
| Callback page | The minimum requirement is for the page to not be redirected to a URL without the `redirect_uri` since the parent window will poll for the redirect. |

## Server-Side Web Apps

In server-side web app such as PHP, Rails, Django, etc. where the operations occur are slightly different.

| Page | Description |
|------|-------------|
| Login page | This is any page with a Login button. This page will open the popup and listen for the redirect, after which it will shut down the popup window. There's no need to do any client-side processing except to shutdown the popup and refresh the page. |
| Callback page | The callback query string will be processed server-side. Nothing is needed client-side. |
