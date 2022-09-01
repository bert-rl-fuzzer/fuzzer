<?php
// Connection & Authorization Process **STARTS**
session_start();
include("./helper/connect_class.php");
$Connector = new Connectors;
$db=$Connector->phptodbconnector();
$Auth = new Auth;
if(!$Auth->authenticate($_SESSION,$db)){
    unset($_SESSION);
}
if($Auth->is_authenticated()){
    header("Location: ./example_members_area.php");
}
// Connection & Authorization Process **ENDS**

// Login Process **STARTS**
include("./helper/example_mysql_injection_login_class.php");
$LUser = new LUser;
if($LUser->validateFormRequest($_POST)){
    if($LUser->validateFormFields()){
        if($LUser->loginUser($db)){
            header("Location: ./example_members_area.php");
        }
    }
}
// Login Process **ENDS**
?>
<!DOCTYPE html>

<head>
    <title>FuzzyCrawler Demo: MYSQL Injection Login Example</title>
    <link rel="shortcut icon" type="image/jpg" href="images/favicon.ico" />
    <link rel="stylesheet" href="plugins/bootstrap_v4.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="plugins/fontawesome_v5.15.2/css/all.css">
    <link rel="stylesheet" href="css/components.css">
    <link rel="stylesheet" href="css/example_mysql_injection_login.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body>
    <?php include("./components/navbar.php"); ?>
    <div class="body_content_container">
        <form action="./example_mysql_injection_login.php" method="POST">
            <div class="form_container">
                <div class="login_container">
                    <h2>Login Form</h2><br>
                    <img src="images/login_image.jpg" style="width: 100%;" />
                    <hr>
                    <!-- Sample Error Text Implementation **Starts** -->
                    <p style="font-size: 18px; color: #880000;"><?php echo $LUser->getErrorTxt(); ?></p>
                    <!-- Sample Error Text Implementation **Ends** -->
                    <!-- Sample Field Value Retention Implementation **Starts** -->
                    <div class="form-group">
                        <label for="email" class="login_label">Email:</label><br>
                        <input type="text" id="email" name="email" placeholder="john.doe@example.com ( ' OR 1=1;-- )"
                            class="form-control" value="<?php echo $LUser->getEmail(); ?>">
                    </div>
                    <!-- Sample Field Value Retention Implementation **Ends** -->
                    <div class="form-group">
                        <label for="password" class="login_label">Password:</label><br>
                        <input type="password" id="password" name="password" class="form-control" placeholder="*****"
                            class="">
                    </div>

                    <hr>
                    <input id="loginbtn" name="loginbtn" type="submit" class="btn btn-default login_submit_button"
                        value="Sign In">
                    <br>
                    <div class="clear"></div>
        </form>
    </div>
    </div><br>
    </div>
    <?php include("./components/footer.php"); ?>
</body>
<script src="plugins/jquery_v3.5.1/js/jquery.min.js"></script>
<script src="plugins/bootstrap_v4.0/js/bootstrap.min.js"></script>

</html>