<html>
<head>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <center>
    <?php
        $filename = "/clash-tracker/data/json/war_picks.json";
        $array = json_decode(file_get_contents($filename), true);
        uasort($array, fn($a, $b) =>
            [$b['town_hall'], $b['trophies']] <=> [$a['town_hall'], $a['trophies']]
        );
        echo '<table cellpadding="1" cellspacing="1" border="1">';
        echo '<td>' . 'TH' . '</td>';
        echo '<td>' . 'Name' . '</td>';
        echo '<td>' . 'Percentage Missed' . '</td>';
        echo '<td>' . 'Average Stars' . '</td>';
        echo '<td>' . 'Rating Score' . '</td>';
        echo '</tr>';
        foreach($array as $key => $item) {
            if ($item['in_clan']) {

                $player_score = $item['player_score'];
                $average_stars = $item['time_filtered_average_stars'];

                echo '<tr>';
                    echo '<td>' . $item['town_hall'] . '</td>';
                    echo '<td>' . $item['name'] . '</td>';
                    echo '<td>' . round(($item['misses']/$item['total'])*100) . '%</td>';
                    echo '<td>' . $average_stars . '</td>';
                    echo '<td>' . $player_score . '</td>';
                echo '</tr>';
            }
        }
        echo '</table>';
        echo basename($filename) . " was last updated: " . date ("F d Y H:i:s.", filemtime($filename));
    ?>
    </center>
</body>
</html>