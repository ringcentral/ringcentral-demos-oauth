RingCentral OAuth Demos
=======================

This project provides 3-legged OAuth demos using the [OAuth 2.0](https://tools.ietf.org/html/rfc6749) [Authorization Code flow](https://tools.ietf.org/html/rfc6749#section-1.3.1) for the RingCentral API in various languages using [official and community SDKs](https://developer.ringcentral.com/library/sdks.html).

The authorization code flow is useful for developers because it delegates the entire authentication, authorization, reset password and SAML-based single sign-on (SSO) flows to RingCentral who provides a consistent user experience.

The demos here so far use the popup approach for 3-legged OAuth.

For more information, see the [RingCentral API Developer Guide on Authorization Code Flow](https://developer.ringcentral.com/api-docs/latest/index.html#!#AuthorizationCodeFlow).

Demos are provided for:

* Client-Side Web Apps
  * [JavaScript](https://github.com/grokify/ringcentral-oauth-demos/tree/master/javascript)
* Server-Side Web Apps
  * [Python 2.7 with Bottle](https://github.com/grokify/ringcentral-oauth-demos/tree/master/python-bottle)
  * [Ruby with Sinatra](https://github.com/grokify/ringcentral-oauth-demos/tree/master/ruby-sinatra)

## Client-Side Web Apps

Client-side web apps using JavaScript have a feature in that the callback URL does not need to contain any processing either on the client-side or the server-side. The entire flow can be managed by the parent JavaScript page that is initiating the login.

| Page | Description |
|------|-------------|
| Login page | This is any page with a Login button. This page will open the popup and listen for the redirect. For client-side processing, this page will also retrieve the query string parameters from the callback page. |
| Callback page | The minimum requirement is for the page to not be redirected to a URL without the `redirect_uri` since the parent window will poll for the redirect. |

## Server-Side Web Apps

In server-side web app such as PHP, Rails, Django, etc. where the operations occur are slightly different. In these cases, the callback URL should process the callback to retrieve the authorization code and exchange it for an access token.

| Page | Description |
|------|-------------|
| Login page | This is any page with a Login button. This page will open the popup and listen for the redirect, after which it will shut down the popup window. There's no need to do any client-side processing except to shutdown the popup and refresh the page. |
| Callback page | The callback query string will be processed server-side. Nothing is needed client-side. |
