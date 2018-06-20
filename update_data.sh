#!/bin/sh

./node_modules/.bin/cypress run --browser chrome --spec cypress/integration/std-batting-data.js

mv "c:/users/makut/Downloads/Fangraphs Leaderboard.csv" "c:/Users/makut/Documents/Data/Fangraphs/Batting/2018/Standard Batting Data.csv" && echo "Standard Batting Data Moved Successfully!" || echo "Failed to Move Standard Batting Data"

./node_modules/.bin/cypress run --browser chrome --spec cypress/integration/std-fielding-data.js

mv "c:/users/makut/Downloads/Fangraphs Leaderboard.csv" "c:/Users/makut/Documents/Data/Fangraphs/Fielding/2018/Standard Fielding Data.csv" && echo "Standard Fielding Data Moved Successfully!" || echo "Failed to Move Standard Fielding Data"

./node_modules/.bin/cypress run --browser chrome --spec cypress/integration/std-pitching-data.js

mv "c:/users/makut/Downloads/Fangraphs Leaderboard.csv" "c:/Users/makut/Documents/Data/Fangraphs/Pitching/2018/Standard Pitching Data.csv" && echo "Standard Pitching Data Moved Successfully!" || echo "Failed to Move Standard Pitching Data"