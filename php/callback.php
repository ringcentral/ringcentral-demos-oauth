<?php

use RingCentral\SDK\SDK;

require_once(__DIR__ . '/vendor/autoload.php');

// Parse the .env file
$dotenv = new Dotenv\Dotenv(getcwd());
$dotenv -> load();

function processCode()
{
    if(!isset($_GET['code'])) {
        return;
    }
    $authCode = $_GET['code'];

    $tokenUrl = $_ENV['RC_Server'] . '/restapi/oauth/token';

    $values = array(
        'grant_type'   => 'authorization_code',
        'code'         => $authCode,
        'redirect_uri' => $_ENV['RC_Redirect_Url']
    );

    //url-ify the data for the POST
    foreach($values as $key=>$value) { $valuesString .= $key.'='.urlencode($value).'&'; }
    rtrim($valuesString, '&');

    $apiKey = base64_encode($_ENV['RC_AppKey'] . ':' . $_ENV['RC_AppSecret']);

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $tokenUrl);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
      'Authorization: ' . $apiKey,
      'Accept: application/json',
      'Content-Type: application/x-www-form-urlencoded'
    ));
    curl_setopt($ch, CURLOPT_POST, count($values));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $valuesString);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

    $response = curl_exec($ch);

    $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
    $header = substr($response, 0, $headerSize);
    $body = substr($response, $headerSize);

    //close connection
    curl_close($ch);

    return $body;
}

$result= processCode();

?>