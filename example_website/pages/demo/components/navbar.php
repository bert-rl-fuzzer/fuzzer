<?php
$pagename = basename($_SERVER['PHP_SELF'], ".php");
?>
<nav class="navbar navbar-expand-lg navbar-light bg-light navbar_container">
    <a class="navbar-brand" href="./">
        <img class="navbar_logo" src="images/navbar_logo.png" />
    </a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ml-auto">
            <li class="nav-item">
                <a class="nav-link <?php echo (($pagename=="index")?'navbar_link_active':'navbar_link'); ?>"
                    href="./">Home</a>
            </li>
            <li class="nav-item">
                <a class="nav-link <?php echo (($pagename=="aboutus")?'navbar_link_active':'navbar_link'); ?>"
                    href="./aboutus.php">About</a>
            </li>
            <li class="nav-item dropdown navbar_dropdown_container">
                <a class="nav-link <?php echo ((substr($pagename,0,7)=="example")?'navbar_link_active':'navbar_link'); ?> dropdown-toggle"
                    id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Examples
                </a>
                <div class="dropdown-menu navbar_dropdown" aria-labelledby="navbarDropdown">
                    <a class="dropdown-item navbar_dropdown_item" href="./example_mysql_injection_login.php">MYSQL
                        Injection
                        Login</a>
                    <a class="dropdown-item navbar_dropdown_item" href="./example_mysql_injection_search_box.php">MYSQL
                        Injection
                        Search</a>
                    <a class="dropdown-item navbar_dropdown_item" href="./example_members_area.php">Members Area</a>
                    <a class="dropdown-item navbar_dropdown_item" href="./logout.php">Logout</a>
                </div>
            </li>
            <li class="nav-item">
                <a class="nav-link  <?php echo (($pagename=="documentation")?'navbar_link_active':'navbar_link'); ?>"
                    href="./documentation.php">Documentation</a>
            </li>
            <li class="nav-item">
                <a class="nav-link  <?php echo (($pagename=="contactus")?'navbar_link_active':'navbar_link'); ?>"
                    href="./contactus.php">Contact</a>
            </li>
        </ul>
    </div>
</nav>
<div class="navbar_spacer"></div>