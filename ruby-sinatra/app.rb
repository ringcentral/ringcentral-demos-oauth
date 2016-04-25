#!ruby

require 'sinatra'
require 'multi_json'
require 'ringcentral_sdk'

set :port, ENV['MY_APP_PORT']

# Enter config in .env file
client = RingCentralSdk::REST::Client.new
config = RingCentralSdk::REST::Config.new.load_dotenv
client.set_app_config config.app

get '/' do
  token_json = client.token.nil? \
    ? '' : MultiJson.encode(client.token.to_hash, pretty: true)

  auth_url = client.authorize_url()
  erb :index, locals: {
    authorize_uri: auth_url,
    redirect_uri: client.app_config.redirect_url,
    token_json: token_json}
end

get '/callback' do
  code = params.key?('code') ? params['code'] : ''
  token = client.authorize_code(code) if code
  ''
end
