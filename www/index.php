<html>
<head>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <center>
    <?php
        echo "<a href='war_picks.php'>Click here for war picks</a>";
        if (file_exists("/clash-tracker/data/json/current_war.json")) {
            $filename = "/clash-tracker/data/json/current_war.json";
            echo "<br>This page includes an ongoing war. Data may be incomplete.<br>";
        }
        else
            $filename = "/clash-tracker/data/json/clash.json";
        $array = json_decode(file_get_contents($filename), true);

        # Subsort code, sorts by town hall and then by th trophies.
        #uasort($array, fn($a, $b) =>
        #    [$b['town_hall'], $b['trophies']] <=> [$a['town_hall'], $a['trophies']]
        #);
        uasort($array, fn($a, $b) =>
            $b['trophies'] <=> $a['trophies']
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
                $average_stars = "";
                if (!is_null($item['time_filtered_average_stars']))
                    $average_stars = $item['time_filtered_average_stars'];
                elseif (!is_null($item['average_stars'])) {
                    $average_stars = $item['average_stars'] . "*";
                    $player_score = $player_score . "*";
                }

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
        echo "* filtered data is empty, no recent attacks. Using player lifetime values<br>";
        echo basename($filename) . " was last updated: " . date ("F d Y H:i:s.", filemtime($filename));
    ?>
    </center>
</body>
</html>