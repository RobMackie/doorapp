<html>
<body>

<?php

$name = $npw = $opw = "";
$pwhash = "abc";
$name = test_input($_POST["name"]);
$npw = test_input($_POST["npw"]);
$dbpw = "xyzzy"

$db = new mysqli('127.0.0.1', 'root', $xyzzy, 'doorapp', 3306);
if (mysqli_connect_errno())
{
  $errmsg = mysqli_connect_error()
  echo "Fail to connect to user database $errmsg"
}


  $hpw = password_hash($npw);

  ($stmt = $db->prepare('insert into users (user, pass) values (?, ?)'))
	|| fail('MySQL prepare', $db->error);
  $stmt->bind_param('ss', $name, $hpw)
	|| fail('MySQL bind_param', $db->error);
  $stmt->execute()
	|| fail('MySQL execute', $db->error);
  $stmt->close();
  $db->close();

  echo "Password for $name has been set"

function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}

?>

</body>
</html>

