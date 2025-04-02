<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google-Style Login</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #202124;
            font-family: 'Roboto', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background-color: #292a2d;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            color: white;
            width: 350px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        .login-container h2 {
            margin-bottom: 10px;
        }
        .login-container input {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border-radius: 5px;
            border: 1px solid #5f6368;
            background-color: #202124;
            color: white;
        }
        .login-container input:focus {
            outline: none;
            border-color: #8ab4f8;
        }
        .login-container button {
            width: 100%;
            padding: 10px;
            margin-top: 20px;
            background-color: #8ab4f8;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            color: black;
        }
        .login-container button:hover {
            background-color: #669df6;
        }
        .options {
            margin-top: 10px;
        }
        .options a {
            color: #8ab4f8;
            text-decoration: none;
            font-size: 14px;
        }
        .options a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Hi Samuel</h2>
        <p>To continue, first verify it's you</p>
        <form action="/login" method="POST">
            <input type="password" name="password" placeholder="Enter your password" required>
            <button type="submit">Next</button>
        </form>
        <div class="options">
            <a href="#">Try another way</a>
        </div>
    </div>
</body>
</html>
