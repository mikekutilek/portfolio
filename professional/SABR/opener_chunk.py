import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sys
import json
import fangraphs as fg
import savant as sa
import argparse

def get_team_rotation_wOBA():
	page = sa.get_page(position='SP', group_by='team', sort_col='woba')
	data = sa.get_table(page)
	new_data = pd.DataFrame()
	new_data['Player'] = data['Player']
	new_data['wOBA'] = data['wOBA'].astype('float64')
	return new_data

def get_team_wOBA_chunk(team):
	data = get_team_rotation_wOBA()
	chunk_data = np.array_split(data, 5)
	if (chunk_data[4]['Player'] == team).any():
		return "starting rotation is in the upper echelon of MLB in wOBA. They probably don't need an opener, but you can still take a look at potential options."
	elif (chunk_data[3]['Player'] == team).any():
		return "starting rotation is in one of the higher tiers of MLB in wOBA. They may or may not need an opener to fill a void, but you can still take a look at potential options."
	elif (chunk_data[2]['Player'] == team).any():
		return "starting rotation is in the middle of MLB in wOBA. They might need an opener to fill a void. Check out their options below!"
	elif (chunk_data[1]['Player'] == team).any():
		return "starting rotation is in one of the lower tiers of MLB in wOBA. They could probably use an opener to fill a void. See options below!"
	elif (chunk_data[0]['Player'] == team).any():
		return "starting rotation is at the very bottom of MLB in wOBA. They definitely have a rotation spot that could be better utilized. See options below!"
	else:
		return "Invalid team. Please try again."

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("team", help="team of candidates you want to find")
	args = parser.parse_args()

	chunk = get_team_wOBA_chunk(args.team)
	opener_data = {"chunk": ""}

	opener_data['chunk'] = chunk

	print(json.dumps(opener_data))
	sys.stdout.flush()

if __name__ == '__main__':
	main()