<html>
<head>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <center>
    <?php
        if (file_exists("/clash-tracker/data/json/current_war.json")) {
            $filename = "/clash-tracker/data/json/current_war.json";
            print_r("This page includes an onging war. Data may be incomplete.");
        }
        else {
            $filename = "/clash-tracker/data/json/clash.json";
        }
        $array = json_decode(file_get_contents($filename), true);
        usort($array, function ($a, $b) {
            return strcmp(strtolower($a["name"]), strtolower($b["name"]));
        });
        echo '<table cellpadding="1" cellspacing="1" border="1">';
        echo '<td>' . 'Name' . '</td>';
        #echo '<td>' . 'Misses' . '</td>';
        #echo '<td>' . 'Total' . '</td>';
        echo '<td>' . 'Percentage Missed' . '</td>';
        echo '<td>' . 'Average Stars' . '</td>';
        echo '<td>' . 'Rating Score' . '</td>';
        echo '</tr>';
        foreach($array as $key => $item) {
            if ($item['in_clan']) {
                echo '<tr>';
                    echo '<td>' . $item['name'] . '</td>';
                    #echo '<td>' . $item['misses'] . '</td>';
                    #echo '<td>' . $item['total'] . '</td>';
                    echo '<td>' . round(($item['misses']/$item['total'])*100) . '%</td>';
                    echo '<td>' . $item['average_stars'] . '</td>';
                    echo '<td>' . $item['player_score'] . '</td>';
                echo '</tr>';
            }
        }
        echo '</table>';
        echo basename($filename) . " was last updated: " . date ("F d Y H:i:s.", filemtime($filename));
    ?>
    </center>
</body>
</html>