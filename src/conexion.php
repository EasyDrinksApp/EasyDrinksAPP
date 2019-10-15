<?php 
ini_set("display_errors", "on");
$hostname 	= 'ec2-23-21-91-183.compute-1.amazonaws.com';
$database   = 'd99im3kf48j37';
$username 	= 'jyoaemdhbzzmmo';
$password 	= 'b7dfc5cb281e23651d3ce373469a74dd82a7ec880831d3d2b2fbeebdbbf16aca';
$port       = '5432';

    try {
        $con = new PDO("pgsql:host=$hostname;port=$port;dbname=$database", $username, $password);
        print "Conexión exitosa!";
        
    }
    catch (Exception $e) {
        print "¡Error!: " . $e->getMessage();
    }   
?>