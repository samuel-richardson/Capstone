<<!DOCTYPE html>
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
  <title>Google Sign In</title>
  <link rel="icon" type="image/png" href="https://cdn-icons-png.flaticon.com/256/2702/2702602.png">
  <style>
    body {
      background-color: white;
      font-family: Roboto, Arial, sans-serif;
      margin: 0;
      padding: 0;
    }

    .popup {
      width: 400px;
      margin: 100px auto;
      border: 1px solid #ddd;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }

    .popup-content {
      padding: 40px;
    }

    .ms-header {
      display: flex;
      align-items: center;
      margin-bottom: 30px;
    }

    .ms-header img {
      height: 30px;
      margin-right: 8px;
    }

    .ms-header span {
      font-size: 22px;
      font-weight: 500;
    }

    form label {
      display: block;
      margin-bottom: 8px;
      font-size: 14px;
      font-weight: 500;
    }

    form input[type="password"],
    form input[type="text"] {
      width: 100%;
      padding: 10px;
      font-size: 16px;
      margin-bottom: 20px;
      box-sizing: border-box;
      border: 1px solid #ccc;
      border-radius: 4px;
    }

    .links {
      margin-bottom: 20px;
    }

    .links a {
      display: block;
      color: #1a73e8;
      text-decoration: none;
      margin-bottom: 5px;
      font-size: 14px;
    }

    .links a:hover {
      text-decoration: underline;
    }

    .button-row {
      text-align: right;
    }

    .button-row button {
      background-color: #1a73e8;
      color: white;
      border: none;
      padding: 10px 24px;
      font-size: 14px;
      border-radius: 4px;
      cursor: pointer;
    }

    .button-row button:hover {
      background-color: #1669c1;
    }

    .footer {
      text-align: center;
      font-size: 12px;
      color: #777;
      padding: 15px 0;
      border-top: 1px solid #ddd;
    }
  </style>
</head>
<body>
  <!-- Popup Login Window -->
  <div class="popup" id="welcomePopup">
    <div class="popup-content">
      <div class="ms-header">
        <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png" alt="Google Logo">
        <span>Sign in</span>
      </div>

      <form method="GET" action="">
        <label for="email">Email or phone</label>
        <input type="text" id="email" name="email" placeholder="Enter your password" required>

        <div class="links">
          <a href="#">Forgot email?</a>
          <a href="#">Use Guest mode to sign in privately</a>
        </div>

        <input type="hidden" name="email_id" value="<?php echo htmlspecialchars($email_id); ?>">

        <div class="button-row">
          <button type="submit" name="submit" value="1">Next</button>
        </div>
      </form>
    </div>

    <div class="footer">Terms of use | Privacy & cookies</div>
  </div>
</body>
</html>

