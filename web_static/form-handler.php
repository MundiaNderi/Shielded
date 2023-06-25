<?php
$name = $_POST['name'];
$visitor_email = $_POST['email']
$message = $_POST['message']

$email_from = '$visitor_email.\n';

$email_message = 'New message';

$email_body = "User Name: $name.\n".
              "User Email: $visitor_email.\n".
              "User message: $message.\n";


$to = 'sarahngima77@gmail.com';

$headers = "From: $email_from \r\n";

$headers .= "Reply_to: $visitor_email r\n";

mail($to, $email_subject, $email_body, $headers)

header("Location: contact.html")

?>