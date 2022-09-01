<?php
session_start();
unset($_SESSION);
session_destroy();
header("Location: ./example_members_area.php");
?>