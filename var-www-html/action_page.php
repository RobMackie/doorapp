<html>
<body>

<?php

$name = $pw = "";
$pwhash = "abc";
$name = test_input($_POST["name"]);
$pw = test_input($_POST["psw"]);
$dbpw = "xyzzy"

$db = new mysqli('127.0.0.1', 'root', $xyzzy, 'doorapp', 3306);
if (mysqli_connect_errno())
{
  $errmsg = mysqli_connect_error()
  echo "Fail to connect to user database $errmsg"
}


if (password_verify($pw, $pwhash)) {
  echo "Welcome $name"

  shell_exec("/usr/local/bin/gpio -g write 17 1");
  sleep 5
  shell_exec("/usr/local/bin/gpio -g write 17 0");

}
else
{
  echo "Incorrect username/password"
}

function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}

?>

</body>
</html>

