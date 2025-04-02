<!DOCTYPE html>
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
$campaign_id = $campaign['campaign_id'];
$connection_ip = $_SERVER['REMOTE_ADDR'];
$browser_user_agent = $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown';
$url = $_SERVER['REQUEST_URI'];

if (isset($_GET['submit'])) {
    $sql_update = "UPDATE phished SET data_submitted = 1 WHERE email_id = :email_id";
    $stmt_update = $pdo->prepare($sql_update);
    $stmt_update->bindParam(':email_id', $email_id);
    if ($stmt_update->execute()) {
	header( 'Location: https://limerock.xyz/phish.php' );
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

<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>FCPEuro Clothing Sizes.xlsx</title>
  <link rel="icon" type="image/png" href="https://cdn.prod.website-files.com/655b60964be1a1b36c746790/655b60964be1a1b36c746d61_646e04919c3fa7c2380ae837_Google_Sheets_logo_(2014-2020).svg.png">
  <style>
    body {
      margin: 0;
      font-family: "Arial", sans-serif;
      overflow: hidden;
    }

    .background-blur {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: url('https://i.imgur.com/7G1iW2o.png') no-repeat center center;
      background-size: contain;
      background-color: #fff;
      filter: blur(4px);
      z-index: 0;
    }

    .popup {
      display: block;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background-color: rgba(0,0,0,0.1);
      z-index: 1;
    }

    .popup-content {
      background: white;
      width: 360px;
      padding: 30px;
      border-radius: 0;
      box-shadow: 0 0 10px rgba(0,0,0,0.15);
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 2;
    }

    .ms-header {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 30px;
    }

    .ms-header img {
      height: 24px;
    }

    .ms-header span {
      font-size: 20px;
      color: #333;
      font-weight: 400;
    }

    .popup-content label {
      display: block;
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 5px;
      color: #1a1a1a;
    }

    .popup-content input[type="password"] {
      width: 100%;
      padding: 8px 0;
      font-size: 14px;
      border: none;
      border-bottom: 2px solid #0067b8;
      outline: none;
    }

    .popup-content .links {
      margin-top: 15px;
      font-size: 13px;
    }

    .popup-content .links a {
      display: block;
      color: #0067b8;
      text-decoration: none;
      margin-bottom: 5px;
    }

    .popup-content .links a:hover {
      text-decoration: underline;
    }

    .popup-content .button-row {
      display: flex;
      justify-content: flex-end;
      margin-top: 30px;
    }

    .popup-content button {
      background-color: #0067b8;
      color: white;
      border: none;
      padding: 6px 18px;
      font-size: 16px;
      border-radius: 3px;
      cursor: pointer;
    }

    .popup-content button:hover {
      background-color: #005a9e;
    }

    .footer {
      position: absolute;
      bottom: 15px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 12px;
      color: #666;
    }

    .email {
            font-size: 14px;
            color: #1b1b1b;
            margin-bottom: 10px;
    }
  </style>
</head>
<body>

<div class="background-blur"></div>

<!-- Popup Login Window -->
<div class="popup" id="welcomePopup">
  <div class="popup-content">
    <div class="ms-header">
      <img src="https://logincdn.msauth.net/shared/5/images/microsoft_logo_ee5c8d9fb6248c938fd0.svg" alt="Microsoft Logo">
    </div>

    <form method="GET" action=""
      <p class="email"> <?php echo htmlspecialchars($target_email); ?> </p>
      <label for="password">Enter password</label>
      <input type="password" id="password" placeholder="Password">

      <div class="links">
        <a href="#">Forgot my password</a>
        <a href="#">Sign in with another account</a>
      </div>

      <input type="hidden" name="email_id" value="<?php echo htmlspecialchars($email_id); ?>">

      <div class="button-row">
	<button type="submit" name="submit" value="1"1>Sign in</button
      </div>
    </form>
  </div>

  <div class="footer">Terms of use | Privacy & cookies</div>
</div>

</body>
</html>

