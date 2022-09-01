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
// Connection & Authorization Process **ENDS**

?>
<!DOCTYPE html>

<head>
    <title>FuzzyCrawler Demo: Members Area Example</title>
    <link rel="shortcut icon" type="image/jpg" href="images/favicon.ico" />
    <link rel="stylesheet" href="plugins/bootstrap_v4.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="plugins/fontawesome_v5.15.2/css/all.css">
    <link rel="stylesheet" href="css/components.css">
    <link rel="stylesheet" href="css/example_members_area.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body>
    <?php include("./components/navbar.php"); ?>
    <div class="body_content_container">
        <div class="form_container">
            <div class="members_container">
                <h2>Members Area</h2><br>
                <?php if($Auth->is_authenticated()){ ?>
                <img src="images/members_image.jpg" style="width: 100%;" />
                <hr>
                <p>Hello <b><?php echo $Auth->getFirstName()." ".$Auth->getLastName(); ?></b>,</p>
                <p>You are currently logged-in, enjoy your members area privileges.</p>
                <p><b>Only Members Can See This!</b></p>
                <?php }else{ ?>
                <img src="images/nonmembers_image.jpg" style="width: 100%;" />
                <hr>
                <p>Hello <b>Guest</b>,</p>
                <p>You are currently not logged-in, members area access is denied.</p>
                <p><b>Only Members Are Allowed!</b></p>
                <?php } ?>
            </div>
        </div>
    </div>
    <?php include("./components/footer.php"); ?>
</body>
<script src="plugins/jquery_v3.5.1/js/jquery.min.js"></script>
<script src="plugins/bootstrap_v4.0/js/bootstrap.min.js"></script>

</html>