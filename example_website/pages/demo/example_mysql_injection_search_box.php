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

//Search Result Generator Process **STARTS**
include("./helper/example_mysql_injection_search_box_class.php");
$Search = new FAQSearch;
$SearchText = ((isset($_POST["search_box"]))?$_POST["search_box"]:"");
$Search->generateSearchResults($db,$SearchText);
$SResultCount=$Search->getResultCount();
if($SResultCount>0){
    $SQuestions=$Search->getQuestions();
    $SAnswers=$Search->getAnswers();
}
//Search Result Generator Process **ENDS**
?>
<!DOCTYPE html>

<head>
    <title>FuzzyCrawler Demo: MYSQL Injection Search Box Example</title>
    <link rel="shortcut icon" type="image/jpg" href="images/favicon.ico" />
    <link rel="stylesheet" href="plugins/bootstrap_v4.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="plugins/fontawesome_v5.15.2/css/all.css">
    <link rel="stylesheet" href="css/components.css">
    <link rel="stylesheet" href="css/example_mysql_injection_search_box.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body>
    <?php include("./components/navbar.php"); ?>
    <div class="body_content_container">
        <form action="./example_mysql_injection_search_box.php" method="POST">
            <div class="form_container">
                <div class="search_box_container">
                    <h2>FAQ Search</h2>
                    <p>Find And Browse Through Our Frequently Asked Questions.</p>
                    <!-- Sample Error Text Implementation **Starts** -->
                    <p style="font-size: 18px; color: #880000;"><?php //echo $Search->getErrorTxt(); ?></p>
                    <!-- Sample Error Text Implementation **Ends** -->
                    <!-- Sample Field Value Retention Implementation **Starts** -->

                    <div class="input-group">
                        <input type="text" class="form-control navbar_search_input" name="search_box" id="search_box"
                            type="search"
                            placeholder="Search Through Our FAQ Section. [  ')  UNION SELECT Null, email, pass, Null FROM user;--  ]"
                            aria-label="Search" value="<?php echo $SearchText; ?>">
                        <div class="input-group-append">
                            <button class="input-group-text btn navbar_search_button" type="submit">
                                <span class="fa fa-search navbar_search_icon"></span>
                            </button>
                        </div>
                    </div>
                    <!-- Sample Field Value Retention Implementation **Ends** -->

                    <hr><br>
                    <div class="clear"></div>

                    <div class="row">
                        <?php for($i=0;$i<$SResultCount;$i++){ ?>
                        <div class="col-12">
                            <div class="col-12"><b><?php echo $SQuestions[$i]; ?>?</b></div>
                            <div class="col-12">Answer: <?php echo $SAnswers[$i]; ?></div>
                            <hr>
                            <br>
                        </div>
                        <?php } ?>
                        <?php if($SResultCount==0){ ?>
                        <div class="col-12">
                            <div class="col-12"><b>No Results Found</b></div>
                        </div>
                        <?php } ?>
                    </div>



                    <br>
                    <img src="images/product_search_footer_image.jpg" style="width: 100%;" />
                    <hr>

        </form>
    </div>
    </div><br>
    </div>
    <?php include("./components/footer.php"); ?>
</body>
<script src="plugins/jquery_v3.5.1/js/jquery.min.js"></script>
<script src="plugins/bootstrap_v4.0/js/bootstrap.min.js"></script>

</html>