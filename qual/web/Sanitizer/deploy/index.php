<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Budiono Siregar</title>
    <link rel="stylesheet" href="style.css">
    
</head>
<body>
    <?php
        $blacklists = ["img", "script", "svg", "frame", "body", "br", "td", "table", "link", "base"];
        $name = "budiono siregar";

        if ($_SERVER["REQUEST_METHOD"] == "GET") {
            if (!empty($_GET["name"])) {
                if (strlen($_GET['name']) > 500) {
                    echo 'Namamu Terlalu Panjang';
                    die();
                }
                $request_name = strtolower($_GET['name']);
                foreach ($blacklists as $blacklist) {
                    while (strpos($request_name, $blacklist) !== false) {
                        echo htmlspecialchars("Ga boleh pake nama ini '".$request_name."' ya kawan!!");
                        $request_name = str_replace($blacklist, '', $request_name);
                    }
                }
            }
        }
        if (!empty($request_name)){
            $name = $request_name;
        }
	$nonce = bin2hex(random_bytes(32));
        $csp_header = "Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-" . $nonce . "'; style-src 'self';";
        header($csp_header);
    ?>
    <div class="container">
        <h1>Perkenalkan nama saya <span id="h1"></span>, cita-cita saya kapal lawd</h1>
        <form method="get" action="">
            <input type="text" name="name" placeholder="Enter your name" required>
            <input type="submit" value="Update Name">
        </form>
        <script src="https://cure53.de/purify.js" nonce="<?php echo $nonce; ?>"></script>
        <script nonce="<?php echo $nonce; ?>">
            var name = <?php echo json_encode($name); ?>;
            if (name) {
                name = DOMPurify.sanitize(name);
                name = name.replace(/>/, "");
                document.getElementById("h1").innerHTML = name
            }
            else {
                document.getElementById("h1").innerHTML = "budiono siregar"
            }
        </script>
    </div>
</body>
</html>
