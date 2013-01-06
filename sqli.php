<?php
/*
mysql> select * from sqli.users;
+------+--------+----------+----------+-------+
| id   | nombre | apellido | password | pin   |
+------+--------+----------+----------+-------+
|    1 | matias | lang     | secret   |  1204 |
|    2 | jose   | gomez    | secret2  | 12345 |
+------+--------+----------+----------+-------+
2 rows in set (0.00 sec)
*/
$con = mysql_connect("localhost", "root", "xxxxx") or die("Error en la conexion");
mysql_select_db('sqli',$con);
if(isset($_GET['id']))
{
    $result = mysql_query("SELECT nombre,apellido from users WHERE id=".$_GET['id'],$con);
    if(mysql_fetch_array($result)){
        echo "Nombre: ".mysql_result($result,0,'nombre').'<br>';
        echo "Apellido: ".mysql_result($result,0,'apellido');
    }else{
        echo "No hay resultados";
    }
}
?>
