<?php

use RingCentral\SDK\SDK;

require_once(__DIR__ . '/vendor/autoload.php');

session_start();

// Parse the .env file
$dotenv = new Dotenv\Dotenv(getcwd());
$dotenv -> load();

function processCode()
{
    if(!isset($_GET['code'])) {
        echo "The auth code is not genrated " . PHP_EOL;
        return;
    }
    $authCode = $_GET['code'];
    echo "The authCode is :" . $_GET['code'] . PHP_EOL;   

    $tokenUrl = $_ENV['RC_Server'] . '/restapi/oauth/token';
    echo "The tokenURL is :" . $tokenUrl . PHP_EOL;
    
    $values = array(
        'grant_type'   => 'authorization_code',
        'code'         => $authCode,
        'redirect_uri' => $_ENV['RC_Redirect_Url']
    );

    //url-ify the data for the POST
    // foreach($values as $key=>$value) { $valuesString .= $key.'='.urlencode($value).'&'; }
    // rtrim($valuesString, '&');

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

    $response = curl_exec($ch);

    $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
    echo "The Header size is :" . $headerSize . PHP_EOL;
    
    $header = substr($response, 0, $headerSize);
    echo "The header is :" . $header . PHP_EOL;
    
    $body = substr($response, $headerSize);
    echo "The body is :" . json_encode($body) . PHP_EOL;
    
    //close connection
    curl_close($ch);

    //Store the response in PHP Session Object
    $_SESSION['response'] = $body;

    echo "The variable stored in session is " . $_SESSION['response'] . PHP_EOL;

    return $body;

}

$result= processCode();

?>

