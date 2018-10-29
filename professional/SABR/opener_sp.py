import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sys
import json
import fangraphs as fg
import savant as sa
import argparse


def get_all_pitchers():
	"""
	This method takes the full active pitcher list from fangraphs
	"""
	#p1 = fg.get_all_pitchers_page()
	p2 = fg.get_all_active_pitchers_page()
	#df = fg.get_table(p1)
	df = fg.get_table(p2)
	active_df = pd.DataFrame()
	active_df['Name'] = df['Name']
	active_df['Team'] = df['Team']
	#print(active_df)
	active_df['fullname'] = ''
	for index, row in active_df.iterrows():
		#print(row)
		"""
		if row['Team'] != '- - -':
			row['Team'] = sa.get_team(row['Team'])
		elif row['Team'] == '- - -':
			player = active_df.loc[active_df['Name'] == row['Name']]
			row['Team'] = sa.get_team(player['Team'].to_string(index=False))
		else:
			row['Team'] = sa.get_team('NA')
		print(row['Name'], row['Team'])
		"""
		active_df.loc[index, 'fullname'] = row['Name'].replace(' ', '').strip().lower()
		row['Team'] = sa.get_team(row['Team'])
		#print(row['Team'])
	return active_df

def get_sps_wOBA_vs(batter_stands):
	page = sa.get_page(batter_stands=batter_stands, position='SP', hfInn='1%7C', min_results='30', sort_col='woba')
	data = sa.get_table(page)
	new_data = pd.DataFrame()
	new_data['Player'] = data['Player']
	new_data['wOBA'] = data['wOBA'].astype('float64').apply(lambda x: '{0:.3f}'.format(x))
	return new_data.loc[new_data['wOBA'].astype('float64') > 0.350]

def get_all_candidates(batter_stands, position):
	df = get_all_pitchers()
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
	args = parser.parse_args()

	sp_rdf = get_team_candidates(args.team, 'R', 'SP')
	sp_ldf = get_team_candidates(args.team, 'L', 'SP')
	#chunk = get_team_wOBA_chunk(args.team)
	opener_data = {"sp_righties": [], "sp_lefties": []}

	for index, r in sp_rdf.iterrows():
		opener_data['sp_righties'].append(r.to_json())

	for index, l in sp_ldf.iterrows():
		opener_data['sp_lefties'].append(l.to_json())

	#opener_data['chunk'] = chunk

	print(json.dumps(opener_data))
	#print(rdf)
	#print(ldf.to_json(orient='records'))
	sys.stdout.flush()
	#print(get_rps_good_vs('R'))
	"""
	page = fg.get_splits_page(args.pid)
	data = fg.get_split_data(page, "tto")
	print(get_TTO_slash(data))
	"""

if __name__ == '__main__':
	main()