<html>
<body>

<?php

$name = $npw = $opw = "";
$pwhash = "abc";
$name = test_input($_POST["name"]);
$opw = test_input($_POST["opw"]);
$npw = test_input($_POST["npw"]);
$dbpw = "xyzzy"

if (strlen($npw)<8)
{
 echo "Password muse be 8 characters"
}
else
{

$db = new mysqli('127.0.0.1', 'root', $xyzzy, 'doorapp', 3306);
if (mysqli_connect_errno())
{
  $errmsg = mysqli_connect_error()
  echo "Fail to connect to user database $errmsg"
}


if (password_verify($opw, $pwhash)) {
  $newhash = password_hash($npw);


  ($stmt = $db->prepare('update  users set pass=? where user=?'))
	|| fail('MySQL prepare', $db->error);
  $stmt->bind_param('ss', $newhash, $name)
	|| fail('MySQL bind_param', $db->error);
  $stmt->execute()
	|| fail('MySQL execute', $db->error);
  $stmt->close();
  $db->close();

  echo "Password for $name has been set"
}
else
{
  echo "Incorrect username/password"
}

} //end else of pw length

function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}

?>

</body>
</html>

