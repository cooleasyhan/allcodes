<?php
    ini_set('display_errors', 'On');

    error_reporting(E_ALL); ini_set( 'display_errors', 'On' );

    echo shell_exec('cindex 2>&1 1>&1 0>&1');
    $result = shell_exec('/usr/bin/csearch php 2>&1 1>&1 0>&1');
    echo $result;

echo '<p>';
    echo shell_exec("sed -n '3,10p' /u01/www/index.php");
echo '</p>';
#    echo phpinfo();
?>
