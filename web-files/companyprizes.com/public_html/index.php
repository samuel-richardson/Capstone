<?php

// Database connection settings
$host = '127.0.0.1';
$port = 3306;
$dbname = 'mailer';
$username = 'mailer_user';
$password = '';

try {
    $pdo = new PDO("mysql:host=$host;port=$port;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Database connection failed: " . $e->getMessage());
}

if (!isset($_GET['email_id']) || empty($_GET['email_id'])) {
    die("You do not have permission to view this site.");
}

$email_id = $_GET['email_id'];

$sql_check = "SELECT * FROM Sent_Emails WHERE email_id = :email_id LIMIT 1";
$stmt_check = $pdo->prepare($sql_check);
$stmt_check->bindParam(':email_id', $email_id);
$stmt_check->execute();
$sent_email = $stmt_check->fetch(PDO::FETCH_ASSOC);

if (!$sent_email) {
    die("You do not have permission to view this site.");
}


$target_first = $sent_email['target_first'];
$target_last = $sent_email['target_last'];
$target_email = $sent_email['target_email'];
$campaign_id = $sent_email['campaign_id'];
$connection_ip = $_SERVER['REMOTE_ADDR'];
$browser_user_agent = $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown';
$url = $_SERVER['REQUEST_URI'];

if (isset($_GET['submit'])) {
    $sql_update = "UPDATE phished SET data_submitted = 1 WHERE email_id = :email_id";
    $stmt_update = $pdo->prepare($sql_update);
    $stmt_update->bindParam(':email_id', $email_id);
    if ($stmt_update->execute()) {
	header( 'Location: https://generator-vt.com/phish.php' );
        // echo "You've been phished as part of a phishing simulation none of your data has been stored please contact you IT admin if you have any further concerns.";
        exit;
    } else {
        echo "Error updating submission status.";
        exit;
    }
}

$sql = "INSERT INTO phished (email_id, campaign_id, connection_ip, browser_user_agent, url, time)
        VALUES (:email_id, :campaign_id, :connection_ip, :browser_user_agent, :url, NOW())";

$stmt = $pdo->prepare($sql);
$stmt->bindParam(':email_id', $email_id);
$stmt->bindParam(':campaign_id', $campaign_id, PDO::PARAM_INT);
$stmt->bindParam(':connection_ip', $connection_ip);
$stmt->bindParam(':browser_user_agent', $browser_user_agent);
$stmt->bindParam(':url', $url);

try {
    $stmt->execute();
} catch (PDOException) {
    //echo "Already recived connection.";
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Phishing Test</title>
  <style>
    html, body {
      height: 100%;
      margin: 0;
      font-family: Arial, sans-serif;
      background: url('https://www.burlingtonfreepress.com/gcdn/-mm-/46728c03b2e0218a281fa297016dc18e19cfed43/c=0-335-4435-2830/local/-/media/2016/05/12/Burlington/B9322048870Z.1_20160512144213_000_GKFEA1FHR.1-0.jpg') no-repeat center center fixed;
      background-size: cover;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .message-box {
      background-color: rgba(0, 0, 0, 0.7);
      color: white;
      padding: 30px;
      border-radius: 12px;
      max-width: 500px;
      text-align: center;
      box-shadow: 0 0 20px rgba(0,0,0,0.5);
    }
  </style>
</head>
<body>
  <div class="message-box">
    <h2>You've been phished!</h2>
    <p>Don't worry, your systems administrators are aware. This was done for testing purposes and is completely anonymous. Contact: mason@generatorvt.com</p>
  </div>
</body>
</html>

