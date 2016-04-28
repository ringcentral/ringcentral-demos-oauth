using Nancy.Hosting.Self;
using Newtonsoft.Json;
using RazorEngine;
using RazorEngine.Templating;
using RestSharp;
using RingCentral.SDK;
using System;
using System.Collections.Generic;
using System.IO;


namespace csharp_nancy
{
    class Program
    {
        static void Main(string[] args)
        {
            var uri = new Uri(string.Format("http://{0}:{1}", Config.Instance.AppHost, Config.Instance.AppPort));

            using (var host = new NancyHost(uri))
            {
                host.Start();

                Console.WriteLine("Your application is running on " + uri);
                Console.WriteLine("Press any [Enter] to close the host.");
                Console.ReadLine();
            }
        }
    }

    public class DefaultModule : Nancy.NancyModule
    {
        private const string MyState = "myState";

        // must be static. Because every time there is new request, a new instance of this class is created.
        static SDK rcsdk = new SDK(Config.Instance.AppKey,
            Config.Instance.AppSecret,
            Config.Instance.ServerUrl,
            "C# OAuth2 demo app", "1.0.0");


        private string AuthorizeUri(string state)
        {
            var baseUrl = Config.Instance.ServerUrl + "/restapi/oauth/authorize";
            var authUrl = string.Format("{0}?response_type=code&state={1}&redirect_uri={2}&client_id={3}",
                baseUrl, Uri.EscapeUriString(state),
                Uri.EscapeUriString(Config.Instance.RedirectUrl),
                Uri.EscapeUriString(Config.Instance.AppKey));
            return authUrl;
        }

        private Dictionary<string, string> GetAuthData(string authCode)
        {
            var client = new RestClient(Config.Instance.ServerUrl);
            var request = new RestRequest("/restapi/oauth/token", Method.POST);

            request.AddHeader("Accept", "application/json");
            request.AddHeader("Content-Type", "application/x-www-form-urlencoded");
            var apiKey = string.Format("{0}:{1}", Config.Instance.AppKey,
                Config.Instance.AppSecret);
            apiKey = Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(apiKey));
            request.AddHeader("Authorization", "Basic " + apiKey);

            request.AddParameter("grant_type", "authorization_code");
            request.AddParameter("redirect_uri", Config.Instance.RedirectUrl);
            request.AddParameter("code", authCode);

            var response = client.Execute(request);
            var authData = JsonConvert.DeserializeObject<Dictionary<string, string>>(response.Content);
            return authData;
        }

        public DefaultModule()
        {
            var authorizeUri = AuthorizeUri(MyState);
            var redirect_uri = Config.Instance.RedirectUrl;
            var template = File.ReadAllText("index.html");
            Get["/"] = _ =>
            {
                var tokenJson = "";
                var authData = rcsdk.GetPlatform().GetAuthData();
                if (authData.ContainsKey("access_token") && authData["access_token"] != null)
                {
                    tokenJson = JsonConvert.SerializeObject(authData, Formatting.Indented);
                }
                var page = Engine.Razor.RunCompile(template, "templateKey", null,
                    new { authorize_uri = authorizeUri, redirect_uri = redirect_uri, token_json = tokenJson });
                return page;
            };
            Get["/callback"] = _ =>
            {
                var authCode = Request.Query.code.Value;
                var newAuthData = GetAuthData(authCode);
                rcsdk.GetPlatform().SetAuthData(newAuthData);
                return ""; // js will close this window and reload parent window
            };
        }
    }
}
