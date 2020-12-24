# Simple TrueSkill Calculator for 1 vs. 1 Matches

[TrueSkill](http://research.microsoft.com/en-us/projects/trueskill) is an algorithm designed to estimate skill in multiplayer games. This specific calculator is a simple tool to calculate rankings given a match history file. 

## Requirements and Setup:

This program requires Python 3 (preferably 3.7+). Once python is installed, install the rest of the requirements by running

`pip install requirements.txt`

## Usage

Set up a match history file (currently `.csv` extension is supported) with the following format:

```
|    Winner    |    Loser    |        Date*        | 
----------------------------------------------------
|  player_1    |  player_2   | 01/01/2020 04:00    |
|  player_3    |  player_4   | 01/03/2020 13:12    | 
|  player_4    |  player_1   | 01/03/2020 20:37    | 
```

**Note**: You can specify whether to let the program sort the rows by a date column or to simply use the order provided. This is critical in order to make sure that rankings are computed sequentially.


After this is complete, simply run

`python src/calculate_trueskill.py <path_to_match_history> <path_to_save_rankings>`

and the completed rankings file will be placed in the `<path_to_save_rankings>` file.

By default, the program will sort by the Date column (the third column in the Match History file). If you would like to disable this functionality, simply use the following switch:

`python src/calculate_trueskill.py -s <path_to_match_history> <path_to_save_rankings>`
 
or

`python src/calculate_trueskill.py --sort <path_to_match_history> <path_to_save_rankings>`


## Acknowledgements
https://github.com/sublee/trueskill
