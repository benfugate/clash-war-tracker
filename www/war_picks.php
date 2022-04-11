<html>
<head>
    <link rel="stylesheet" href="styles.css">
    <style>
        @media screen and (min-width: 600px) {
            table {
                width: 100%;
            }
            td {
                font-size: 26px;
                padding: 5px;
            }
        }
        @media screen and (min-width: 1280px) {
            table {
                width: 30%;
            }
            td {
                font-size: 16px;
                padding: 0px;
            }
        }
    </style>
</head>
<body>
    <center>
    <?php
        echo "<a href='index.php'>Click here to see clan war stats</a>";
        $filename = "/clash-tracker/data/json/war_picks.json";
        $array = json_decode(file_get_contents($filename), true);
        uasort($array, fn($a, $b) =>
            [$b['trophies']] <=> [$a['trophies']]
        );
        echo '<table cellpadding="1" cellspacing="1" border="1">';
        echo '<td>' . '#' . '</td>';
        echo '<td>' . 'TH' . '</td>';
        echo '<td>' . 'Name' . '</td>';
        echo '<td>' . 'Percentage<br>Missed' . '</td>';
        echo '<td>' . 'Average<br>Stars' . '</td>';
        echo '<td>' . 'Rating<br>Score' . '</td>';
        echo '<td>' . 'Last War' . '</td>';
        echo '</tr>';
        $index = 1;
        foreach($array as $key => $item) {
            if ($item['in_war']) {

                $player_score = $item['player_score'];
                $last_war = "";
                if ($item['most_recent_war']) {
                    $last_war = $item['most_recent_war'];
                    $last_war = new DateTime("@$last_war");
                    $last_war = $last_war->format('m-d-Y');
                }
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
                    echo '<td>' . $last_war . '</td>';
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
                $last_war = "";
                if ($item['most_recent_war']) {
                    $last_war = $item['most_recent_war'];
                    $last_war = new DateTime("@$last_war");
                    $last_war = $last_war->format('m-d-Y');
                }
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
                    echo '<td>' . $last_war . '</td>';
                echo '</tr>';
                $index++;
            }
        }
        echo '</table>';

        echo 'Rating Score of -1 indicates new clan member<br>';
        echo "* filtered data is empty, no recent attacks. Using player lifetime values<br>";
        echo basename($filename) . " was last updated: " . date ("F d Y H:i:s.", filemtime($filename));
    ?>
    </center>
</body>
</html>