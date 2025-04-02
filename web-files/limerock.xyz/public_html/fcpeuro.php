<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FCP Euro Support</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: #f9f9f9;
        }

        header {
            background: #fff;
            padding: 10px 20px;
            border-bottom: 1px solid #ddd;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        header img {
            height: 40px;
        }

        .top-nav {
            font-size: 14px;
            display: flex;
            gap: 20px;
        }

        .hero {
            background: url('https://info.fcpeuro.com/hubfs/Brand/Logo%20Pack/PNG/FCP-Euro-Logo-Full-Black.png') no-repeat center;
            background-size: cover;
            height: 400px;
            position: relative;
        }

        .articles {
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
        }

        .articles h2 {
            font-size: 22px;
            margin-bottom: 20px;
        }

        .articles ul {
            columns: 2;
            list-style: none;
            padding: 0;
        }

        .articles li {
            margin-bottom: 10px;
        }

        a {
            text-decoration: none;
            color: #0073e6;
        }

        a:hover {
            text-decoration: underline;
        }

        /* Popup Styles */
        .popup {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: rgba(0,0,0,0.6);
            z-index: 1000;
        }

        .popup-content {
            background: white;
            width: 300px;
            padding: 20px;
            border-radius: 8px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }

        .popup-content input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
        }

        .popup-content button {
            margin-top: 15px;
            padding: 8px 16px;
            background: #0073e6;
            border: none;
            color: white;
            border-radius: 4px;
            cursor: pointer;
        }

        .popup-content button:hover {
            background: #005bb5;
        }

	.hover-link {
	    position: relative;
	    display: inline-block;
	}

	.hover-link .hover-img {
	    display: none;
	    position: absolute;
	    top: 30px;
	    left: 0;
	    width: 100px;
	    border: 1px solid #ccc;
	    background: white;
	    padding: 5px;
	    z-index: 999;
	    box-shadow: 0px 2px 6px rgba(0,0,0,0.2);
	}

	.hover-link:hover .hover-img {
	    display: block;
	}

    </style>
</head>
<body>

<header>
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 20px;">
        <img src="https://info.fcpeuro.com/hubfs/Brand/Logo%20Pack/PNG/FCP-Euro-Logo-Full-Black.png" alt="FCP Euro Logo" style="height: 40px;">
        <div style="display: flex; gap: 20px; font-size: 14px;">
            <a href="#" style="text-decoration: none; color: black;">DIY Blog</a>
            <a href="#" style="text-decoration: none; color: black;">Help Me</a>
            <a href="#" style="text-decoration: none; color: black;">My Account</a>
            <a href="#" style="text-decoration: none; color: black;">🛒</a>
        </div>
    </div>
    <div style="display: flex; justify-content: center; gap: 40px; padding: 10px 0; border-top: 1px solid #ddd; border-bottom: 1px solid #ddd; font-size: 14px;">
        <div>🛞 Free Shipping Over $49</div>
        <div>🔁 Hassle-Free Returns</div>
        <div>🛠️ Lifetime Replacement</div>
    </div>
    <div style="display: flex; justify-content: center; gap: 30px; padding: 10px 0; font-size: 13px;">
        <a href="#" style="text-decoration: none; color: black;">BMW Parts</a>
        <a href="#" style="text-decoration: none; color: black;">Volvo Parts</a>
        <a href="#" style="text-decoration: none; color: black;">VW Parts</a>
        <a href="#" style="text-decoration: none; color: black;">Audi Parts</a>
        <a href="#" style="text-decoration: none; color: black;">Mercedes Parts</a>
        <a href="#" style="text-decoration: none; color: black;">Porsche Parts</a>
    </div>
</header>


<div class="hero"></div>

<!-- Popup -->
<div class="popup" id="welcomePopup">
    <div class="popup-content">
        <h2>Welcome!</h2>
        <p><strong>To claim your company's free apparel, access this spread sheet and input your clothing sizes!</strong></p>
        
        <div class="hover-link">
            <a href="https://google.com" target="_blank">Apparel</a>
            <img src="https://cdn.prod.website-files.com/655b60964be1a1b36c746790/655b60964be1a1b36c746d61_646e04919c3fa7c2380ae837_Google_Sheets_logo_(2014-2020).svg.png" alt="Preview" class="hover-img">
        </div>

        <br>
        <button onclick="closePopup()">Close</button>
    </div>
</div>


<section class="articles">
    <h2>Popular Articles</h2>
    <ul>
        <li><a href="#">Jan 9 USPS Shipping Update</a></li>
        <li><a href="#">What is my order status, how and where do I track it?</a></li>
        <li><a href="#">When will my order ship? Do you have my part in-stock?</a></li>
        <li><a href="#">How to create a return</a></li>
        <li><a href="#">How do I know if a part fits?</a></li>
        <li><a href="#">How long will my pick-up order be held in-store?</a></li>
        <li><a href="#">Can I pick up my order in-store?</a></li>
        <li><a href="#">Can I cancel, change, or add to my order?</a></li>
        <li><a href="#">Can I return used oil under the Lifetime Guarantee?</a></li>
        <li><a href="#">How do I find parts that fit my car?</a></li>
    </ul>
</section>

<script>
    window.onload = function() {
        document.getElementById('welcomePopup').style.display = 'block';
    }

    function closePopup() {
        document.getElementById('welcomePopup').style.display = 'none';
    }
</script>

</body>
</html>

