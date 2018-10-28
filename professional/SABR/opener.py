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
	active_df = fg.get_table(p2)
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

"""
def get_TTO_slash(data):
	s = "wOBA slash: "
	for i in range(len(data)):
		s += data['wOBA'][i]
		if i != len(data) - 1:
			s += "/"
	return s

def get_first_second_diff(data):
	wOBA = data['wOBA'].astype('float64')
	first = wOBA[0]
	second = wOBA[1]
	diff = round(first - second, 3)
	return diff

def determine_sp_candidate(diff):
	if diff >= 0.025 and diff < 0.05:
		s = "might"
	elif diff >= 0.05:
		s ="probably"
	else:
		s = "don't"
	return "You %s need an opener" % s
"""

def get_team_rotation_wOBA():
	page = sa.get_page(position='SP', group_by='team', sort_col='woba')
	data = sa.get_table(page)
	data['wOBA'] = data['wOBA'].astype('float64')
	return data.sort_values(by=['wOBA'], ascending=True)

def get_team_wOBA_chunk(team):
	data = get_team_rotation_wOBA()
	chunk_data = np.array_split(data, 5)
	if (chunk_data[0]['Player'] == team).any():
		return "starting rotation is in the upper echelon of MLB in wOBA. They probably don't need an opener, but you can still take a look at potential options."
	elif (chunk_data[1]['Player'] == team).any():
		return "starting rotation is in one of the higher tiers of MLB in wOBA. They may or may not need an opener to fill a void, but you can still take a look at potential options."
	elif (chunk_data[2]['Player'] == team).any():
		return "starting rotation is in the middle of MLB in wOBA. They might need an opener to fill a void. Check out their options below!"
	elif (chunk_data[3]['Player'] == team).any():
		return "starting rotation is in one of the lower tiers of MLB in wOBA. They could probably use an opener to fill a void. See options below!"
	elif (chunk_data[4]['Player'] == team).any():
		return "starting rotation is at the very bottom of MLB in wOBA. They definitely have a rotation spot that could be better utilized. See options below!"
	else:
		return "Invalid team. Please try again."

def get_rps_wOBA_vs(batter_stands):
	pd.options.display.float_format = '${:,.3f}'.format
	page = sa.get_page(batter_stands=batter_stands, position='RP', min_results='75', sort_col='woba')
	data = sa.get_table(page)
	data['wOBA'] = data['wOBA'].astype('float64').apply(lambda x: '{0:.3f}'.format(x))
	
	return data.sort_values(by=['wOBA'], ascending=True).loc[data['wOBA'].astype('float64') < 0.250]

def get_sps_wOBA_vs(batter_stands):
	page = sa.get_page(batter_stands=batter_stands, position='SP', hfInn='1%7C', min_results='30', sort_col='woba')
	data = sa.get_table(page)
	data['wOBA'] = data['wOBA'].astype('float64').apply(lambda x: '{0:.3f}'.format(x))
	return data.sort_values(by=['wOBA'], ascending=False).loc[data['wOBA'].astype('float64') > 0.350]

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

	rp_rdf = get_team_candidates(args.team, 'R', 'RP')
	#rp_ldf = get_team_candidates(args.team, 'L', 'RP')
	#sp_rdf = get_team_candidates(args.team, 'R', 'SP')
	#sp_ldf = get_team_candidates(args.team, 'L', 'SP')
	#chunk = get_team_wOBA_chunk(args.team)
	opener_data = {"chunk": "", "rp_righties": [], "rp_lefties": [], "sp_righties": [], "sp_lefties": []}

	for index, r in rp_rdf.iterrows():
		opener_data['rp_righties'].append(r.to_json())

	#for index, l in rp_ldf.iterrows():
	#	opener_data['rp_lefties'].append(l.to_json())

	#for index, r in sp_rdf.iterrows():
	#	opener_data['sp_righties'].append(r.to_json())

	#for index, l in sp_ldf.iterrows():
	#	opener_data['sp_lefties'].append(l.to_json())

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