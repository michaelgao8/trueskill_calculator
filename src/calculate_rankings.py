from trueskill import Rating, rate_1vs1
import logging
import pandas as pd 
from pathlib import Path
import numpy as np
import argparse

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

# CLI
parser = argparse.ArgumentParser(description="Calculate Rankings according to TrueSkill given a match history")
parser.add_argument('match_history', type=str, help='.csv file that contains the match history file')
parser.add_argument('saved_rankings', type=str, help='Path to file to save rankings in')
parser.add_argument('-s', '--sort', help='Sort by date (3rd column) to get order of matches', action='store_true')

if __name__ == '__main__':
	args = parser.parse_args()
	match_history_filepath = Path(args.match_history)
	match_history = pd.read_csv(match_history_filepath)
	
	if args.sort:
		match_history.iloc[:, 2] = pd.to_datetime(match_history.iloc[:, 2])
		match_history = match_history.sort_values(match_history.columns[2], axis=0)

	# Create list of all players
	all_players = list(set(list(match_history.iloc[:, 0].unique()) + list(match_history.iloc[:, 1].unique())))
	ranking_dict = {player:Rating() for player in all_players}

	winner_col = match_history.columns[0]
	loser_col = match_history.columns[1]
	win_count = {player:0 for player in ranking_dict}
	loss_count = {player:0 for player in ranking_dict}

	# Update everyone's ratings and sigma values
	for match in match_history.itertuples():
		winner = getattr(match, winner_col)
		loser = getattr(match, loser_col)
		win_count[winner] += 1
		loss_count[loser] += 1
		ranking_dict[winner], ranking_dict[loser] = rate_1vs1(ranking_dict[winner], ranking_dict[loser])

	# Get the final ranking list:
	score_dict = {player: ranking_dict[player].mu - 3*ranking_dict[player].sigma for player in ranking_dict.keys()}
	final_df = pd.concat([pd.Series(score_dict), pd.Series(win_count), pd.Series(loss_count)], axis=1) 
	final_df = final_df.reset_index()
	final_df.columns = ['Player Name', 'TrueSkill', '# Matches won', '# Matches lost']
	final_df = final_df.sort_values('TrueSkill', ascending=False)
	final_df['Rank'] = np.arange(final_df.shape[0]) + 1	
	
	# Save the final rankings file
	saved_rankings = args.saved_rankings.replace(".csv", "")
	final_df.to_csv(f"{saved_rankings}.csv", index=False)	

