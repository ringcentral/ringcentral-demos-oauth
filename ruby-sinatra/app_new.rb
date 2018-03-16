#!ruby

require 'dotenv'
require 'sinatra'
require 'multi_json'
require 'ringcentral'

# Create and edit the .env file:
# $ cp config-sample.env.txt .env

Dotenv.load(ENV['ENV_PATH'] || '.env')

rc = RingCentral.new(
  ENV['RINGCENTRAL_CLIENT_ID'],
  ENV['RINGCENTRAL_CLIENT_SECRET'],
  ENV['RINGCENTRAL_SERVER_URL']
)

set :logger, Logger.new(STDOUT)
set :port, ENV['RINGCENTRAL_CLIENT_PORT']

get '/' do
  token_json = rc.token.nil? \
    ? '' : MultiJson.encode(rc.token.to_hash, pretty: true)

  state = rand(1000000)
  logger.info("OAuth2 Callback Request State #{state}")

  erb :index, locals: {
    authorize_uri: rc.authorize_uri(ENV['RINGCENTRAL_CLIENT_REDIRECT_URL'], state),
    redirect_uri: ENV['RINGCENTRAL_CLIENT_REDIRECT_URL'],
    token_json: token_json}
end

get '/callback' do
  code  = params.key?('code')  ? params['code'] : ''
  state = params.key?('state') ? params['state'] : ''
  token = rc.authorize(auth_code: code) if code
  logger.info("OAuth2 Callback Response State #{state}")
  ''
end
