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
            [$b['trophies']] <=> [$a['trophies']]
        );
        echo '<table cellpadding="1" cellspacing="1" border="1">';
        echo '<td>' . '' . '</td>';
        echo '<td>' . 'TH' . '</td>';
        echo '<td>' . 'Name' . '</td>';
        echo '<td>' . 'Percentage Missed' . '</td>';
        echo '<td>' . 'Average Stars' . '</td>';
        echo '<td>' . 'Rating Score' . '</td>';
        echo '</tr>';
        $index = 1;
        foreach($array as $key => $item) {
            if ($item['in_war']) {

                $player_score = $item['player_score'];
                $average_stars = "";
                if (!is_null($item['time_filtered_average_stars']))
                    $average_stars = $item['time_filtered_average_stars'];
                elseif (!is_null($item['average_stars'])) {
                    $average_stars = $item['average_stars'] . "*";
                    $player_score = $player_score . "*";
                }

                echo '<tr>';
                    echo '<td>' . $index . '</td>';
                    echo '<td>' . $item['town_hall'] . '</td>';
                    echo '<td>' . $item['name'] . '</td>';
                    echo '<td>' . round(($item['misses']/$item['total'])*100) . '%</td>';
                    echo '<td>' . $average_stars . '</td>';
                    echo '<td>' . $player_score . '</td>';
                echo '</tr>';
                $index++;
            }
        }
        echo '</table>';
        echo 'Excess players filtered out of war';
        echo '<table cellpadding="1" cellspacing="1" border="1">';
        foreach($array as $key => $item) {
            if (!$item['in_war']) {

                $player_score = $item['player_score'];
                $average_stars = "";
                if (!is_null($item['time_filtered_average_stars']))
                    $average_stars = $item['time_filtered_average_stars'];
                elseif (!is_null($item['average_stars'])) {
                    $average_stars = $item['average_stars'] . "*";
                    $player_score = $player_score . "*";
                }

                echo '<tr>';
                    echo '<td>' . $index . '</td>';
                    echo '<td>' . $item['town_hall'] . '</td>';
                    echo '<td>' . $item['name'] . '</td>';
                    echo '<td>' . round(($item['misses']/$item['total'])*100) . '%</td>';
                    echo '<td>' . $average_stars . '</td>';
                    echo '<td>' . $player_score . '</td>';
                echo '</tr>';
                $index++;
            }
        }
        echo '</table>';

        echo 'Rating Score of -1 indicates new clan member<br>';
        echo "* filtered data is empty, no recent attacks. Using player lifetime values<br>";
        echo basename($filename) . " was last updated: " . date ("F d Y H:i:s.", filemtime($filename));
        echo "<br><a href='index.php'>Click here to go to the homepage</a>";
    ?>
    </center>
</body>
</html>