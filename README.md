RingCentral OAuth Demos
=======================

This project provides OAuth 2.0 demos for the RingCentral API in various languages.

## Client-Side Web Apps

| Page | Description |
|------|-------------|
| Login page | This is any page with a Login button. This page will open the popup and listen for the redirect. For client-side processing, this page will also retrieve the query string parameters from the callback page. |
| Callback page | For client-side processing, this page can be anywhere but it shouldn't be redirected to a URL without the `redirect_uri` in it given the client-side polling implementation. |

## Server-Side Web Apps

In server-side web app such as PHP, Rails, Django, etc. where the operations occur are slightly different.

| Page | Description |
|------|-------------|
| Login page | This is any page with a Login button |
| Callback page | While the callback page does not need to return any data as the popup will be closed, the query string does need to be processed on the server side so the `access_token` can be loaded into the server-side app. |