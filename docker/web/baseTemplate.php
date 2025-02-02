<?php

// Database connection settings
$host = '127.0.0.1';
$port = 3306;
$dbname = 'mailer';
$username = 'mailer_user';
$password = 'LBbY5uAWLNc!pBaU@5X!tS';

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

$sql_check = "SELECT campaign_id FROM Sent_Emails WHERE email_id = :email_id LIMIT 1";
$stmt_check = $pdo->prepare($sql_check);
$stmt_check->bindParam(':email_id', $email_id);
$stmt_check->execute();
$campaign = $stmt_check->fetch(PDO::FETCH_ASSOC);

if (!$campaign) {
    die("You do not have permission to view this site.");
}

$campaign_id = $campaign['campaign_id'];
$connection_ip = $_SERVER['REMOTE_ADDR'];
$browser_user_agent = $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown';
$url = $_SERVER['REQUEST_URI'];

if (isset($_GET['submit'])) {
    $sql_update = "UPDATE phished SET data_submitted = 1 WHERE email_id = :email_id";
    $stmt_update = $pdo->prepare($sql_update);
    $stmt_update->bindParam(':email_id', $email_id);
    if ($stmt_update->execute()) {
        echo "You've been phished as part of a phishing simulation none of your data has been stored please contact you IT admin if you have any further concerns.";
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

<!-- HTML Form to Confirm Data Submission -->
<form method="GET" action="">
    <input type="hidden" name="email_id" value="<?php echo htmlspecialchars($email_id); ?>">
    <button type="submit" name="submit" value="1">Confirm Submission</button>
</form>
