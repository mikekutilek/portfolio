import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sys
import json
import fangraphs as fg
import savant as sa
import baseballref as br
import sabr
import argparse

pd.options.mode.chained_assignment = None

def get_all_batter_fps():
	page = br.get_std_batting_page()
	batters = br.get_player_table(page)

	field_page = br.get_std_fielding_page()
	fielders = br.get_player_table(field_page)

	of_page = br.get_of_fielding_page()
	ofs = br.get_player_table(of_page)

	df2 = pd.merge(batters, ofs[['A', 'Name']], on=['Name'], how='left').fillna(0)
	df2.rename(columns={'A':'OFA'}, inplace=True)
	df3 = pd.merge(df2, fielders[['A', 'E', 'Name']], on=['Name'], how='left').fillna(0)

	#batting and fielding data
	players = df3['Name'].astype('str')
	games = df3['G'].astype('float64')
	r = df3['R'].astype('float64')
	
	double = df3['2B'].astype('float64')
	triple = df3['3B'].astype('float64')
	homer = df3['HR'].astype('float64')
	single = df3['H'].astype('float64') - double - triple - homer
	rbi = df3['RBI'].astype('float64')
	sb = df3['SB'].astype('float64')
	cs = df3['CS'].astype('float64')
	bb = df3['BB'].astype('float64')
	hbp = df3['HBP'].astype('float64')
	so = df3['SO'].astype('float64')

	e = df3['E'].astype('float64')
	ofa = df3['OFA'].astype('float64')
	a = df3['A'].astype('float64')
	

	fps = r + single + (double * 2) + (triple * 3) + (homer * 4) + rbi + (sb * 1.75) - (cs * 0.5) + (bb * 0.75) + (hbp * 0.5) - (so * .1) - e + (ofa * 1) + (a * 0.05)
	fps_g = fps / games

	df = build_fp_table(players, fps, fps_g)

	return df

def get_all_pitcher_fps():
	page = br.get_standard_pitching_page()
	pitchers = br.get_player_table(page)

	relief_page = br.get_relief_page()
	relievers = br.get_player_table(relief_page)

	qs_page = br.get_starting_page()
	qs_table = br.get_player_table(qs_page)

	sb_page = br.get_sb_pitching_page()
	sb_table = br.get_player_table(sb_page)

	df2 = pd.merge(pitchers, relievers[['Hold', 'BSv', 'Name']], on=['Name'], how='left').fillna(0)
	df3 = pd.merge(df2, qs_table[['QS', 'Name']], on=['Name'], how='left').fillna(0)
	df4 = pd.merge(df3, sb_table[['SB', 'Name']], on=['Name'], how='left').fillna(0)
	#print(list(df3))

	players = df3['Name'].astype('str')
	games = df3['G'].astype('float64')
	ip = df3['IP'].astype('float64')
	w = df3['W'].astype('float64')
	l = df3['L'].astype('float64')
	cg = df3['CG'].astype('float64')
	sv = df3['SV'].astype('float64')
	h = df3['H'].astype('float64')
	er = df3['ER'].astype('float64')
	walks = df3['BB'].astype('float64')
	hb = df3['HBP'].astype('float64')
	k = df3['SO'].astype('float64')

	hld = df3['Hold'].astype('float64')
	bsv = df3['BSv'].astype('float64')

	#handling half innings
	half_ip = []
	inns = []
	for i in ip:
		inn = int(i)
		half_i = str(i)[-1]
		inns.append(inn)
		half_ip.append(float(half_i))

	innings = pd.Series(inns)
	rem = pd.Series(half_ip)

	qs = df3['QS'].astype('float64')
	sb = df4['SB'].astype('float64')

	fps = (innings * 1.0) + (rem * 0.33) + (w * 9) - (l * 6) + (cg * 7) + (sv * 8) - (h * 0.25) - er - (walks * 0.5) - (hb * 0.5) + k + (hld * 7.5) - (bsv * 3) + (qs * 5) - (sb * 0.25)
	fps_g = fps / games

	df = build_fp_table(players, fps, fps_g)

	return df

def build_fp_table(players, fps, fps_g):
	df = pd.DataFrame()
	df['Player'] = players
	df['FP'] = fps.apply(lambda x: '{0:.2f}'.format(x)).astype('float64')
	df['FP/G'] = fps_g.apply(lambda x: '{0:.2f}'.format(x)).astype('float64')
	return df

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("ptype", help="type of player (batter or pitcher)")
	parser.add_argument("sort_col", help="category you want to sort by")
	args = parser.parse_args()

	data = []

	if args.ptype == 'batter':
		data = pd.read_json('[{"Player": "Trout", "FP": 1, "FP/G": 2}, {"Player": "Betts", "FP": 3, "FP/G": 4}]')
	elif args.ptype == 'pitcher':
		data = get_all_pitcher_fps()
	else:
		exit(1)

	if args.sort_col == 'FP':
		sort = 'FP'
	elif args.sort_col == 'FPG':
		sort = 'FP/G'

	print(data.sort_values(by=[sort], ascending=False).to_json(orient='records'))
	#print(json.dumps(data))
	sys.stdout.flush()

if __name__ == '__main__':
	main()