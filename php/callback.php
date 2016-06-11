<?php

require_once(__DIR__ . '/vendor/autoload.php');

use RingCentral\SDK\SDK;

session_start();

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

    $apiKey = base64_encode($_ENV['RC_AppKey'] . ':' . $_ENV['RC_AppSecret']);

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $tokenUrl);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
      'Authorization: Basic' . $apiKey,
      'Accept: application/json',
      'Content-Type: application/x-www-form-urlencoded'
    ));
    curl_setopt($ch, CURLOPT_POST, count($values));
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($values));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_VERBOSE, 1);
    curl_setopt($ch, CURLOPT_HEADER, 1);

    $response = curl_exec($ch);

    $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
    $body = substr($response, $headerSize);
    
    //close connection
    curl_close($ch);

    $body = json_encode(json_decode($body, true), JSON_PRETTY_PRINT);

    //Store the response in PHP Session Object
    $_SESSION['response'] = $body;

    return $body;

}

$result= processCode();

session_write_close();

?>

