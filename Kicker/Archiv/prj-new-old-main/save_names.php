<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name1 = $_POST["name1"];
    $name2 = $_POST["name2"];

    $names = "$name1, $name2\n";

    $file = fopen("PlayerNames.txt", "w") or die("Kann Datei nicht öffnen");
    fwrite($file, $names);
    fclose($file);

    echo "Namen erfolgreich gespeichert:<br>$names";
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Namen speichern</title>
</head>
<body>
    <h1>Namen speichern</h1>
    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
        <label for="name1">Name 1:</label>
        <input type="text" id="name1" name="name1"><br><br>
        <label for="name2">Name 2:</label>
        <input type="text" id="name2" name="name2"><br><br>
        <input type="submit" value="Speichern">
    </form>
</body>
</html>
