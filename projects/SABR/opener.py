import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sys
import json
import fangraphs as fg
import savant as sa
import sabr
import argparse

def get_rps_wOBA_vs(batter_stands):
	#pd.options.display.float_format = '${:,.3f}'.format
	page = sa.get_page(batter_stands=batter_stands, position='RP', min_results='75', sort_col='woba')
	data = sa.get_table(page)
	new_data = pd.DataFrame()
	new_data['Player'] = data['Player']
	new_data['wOBA'] = data['wOBA'].astype('float64').apply(lambda x: '{0:.3f}'.format(x))
	
	return new_data.loc[new_data['wOBA'].astype('float64') < 0.250]

def get_sps_wOBA_vs(batter_stands):
	page = sa.get_page(batter_stands=batter_stands, position='SP', hfInn='1%7C', min_results='30', sort_col='woba')
	data = sa.get_table(page)
	new_data = pd.DataFrame()
	new_data['Player'] = data['Player']
	new_data['wOBA'] = data['wOBA'].astype('float64').apply(lambda x: '{0:.3f}'.format(x))
	return new_data.loc[new_data['wOBA'].astype('float64') > 0.350]

def get_all_candidates(batter_stands, position):
	df = sabr.get_all_pitchers()
	if position == 'RP':
		data = get_rps_wOBA_vs(batter_stands)
	else:
		data = get_sps_wOBA_vs(batter_stands)
	data['Team'] = ''
	for index, row in data.iterrows():
		playername = row['Player'].replace(' ', '').strip().lower()
		if not df.loc[df['fullname'] == playername].empty:
			t = df.loc[df['fullname'] == playername].Team.item()
			data.loc[index, 'Team'] = t
	return data

def get_team_candidates(team, batter_stands, position):
	df = get_all_candidates(batter_stands, position)
	if team == 'ANY':
		candidates = df
	else:
		candidates = df.loc[df['Team'] == team]

	return candidates

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("team", help="team of candidates you want to find")
	parser.add_argument("pos", help="position of the player")
	parser.add_argument("hand", help="handedness of the hitter")

	args = parser.parse_args()

	df = get_team_candidates(args.team, args.hand, args.pos)
	opener_data = {"candidates": []}

	for index, r in df.iterrows():
		opener_data['candidates'].append(r.to_json())

	print(json.dumps(opener_data))
	sys.stdout.flush()

if __name__ == '__main__':
	main()