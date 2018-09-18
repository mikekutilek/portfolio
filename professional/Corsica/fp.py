import numpy as np
import pandas as pd
import hockeyref as hr
import sys, json, argparse

def get_all_skater_fps():
	skater_page = hr.get_all_skaters_page()
	skaters = hr.get_table(skater_page)
	skaters = skaters.replace('', 0)
	players = skaters['Player'].astype('str')
	
	games = skaters['GP'].astype('float64')
	goals = skaters['G'].astype('float64')
	assists = skaters['A'].astype('float64')
	pts = skaters['PTS'].astype('float64')
	plus_minus = skaters['+/-'].astype('float64')
	ppg = skaters['PPG'].astype('float64')
	shg = skaters['SHG'].astype('float64')
	gwg = skaters['GW'].astype('float64')
	ppa = skaters['PPA'].astype('float64')
	sha = skaters['SHA'].astype('float64')
	shots = skaters['S'].astype('float64')
	blocks = skaters['BLK'].fillna(0).astype('float64')
	hits = skaters['HIT'].astype('float64')

	fps = (goals * 5) + (assists * 3) + (plus_minus * 1) + (ppg * 2) + (ppa * 2) + (gwg * 2) + (shg * 2) + (sha * 2) + (shots * 0.9) + (blocks * 0.05) + (hits * 0.1)
	fps_g = fps / games

	df = build_fp_table(players, fps, fps_g)

	return df.sort_values(by=['FP/G'], ascending=False)

def get_all_goalie_fps():
	goalie_page = hr.get_all_goalies_page()
	goalies = hr.get_table(goalie_page)
	goalies = goalies.replace('', 0)
	players = goalies['Player'].astype('str')

	games = goalies['GP'].astype('float64')
	wins = goalies['W'].astype('float64')
	losses = goalies['L'].astype('float64')
	otl = goalies['T/O'].astype('float64')
	ga = goalies['GA'].astype('float64')
	saves = goalies['SV'].astype('float64')
	shutouts = goalies['SO'].astype('float64')

	fps = (wins * 5) - (losses * 3) - (ga * 1) + (saves * 0.2) + (shutouts * 8)
	fps_g = fps / games

	df = build_fp_table(players, fps, fps_g)

	return df.sort_values(by=['FP/G'], ascending=False)

def get_skater_fps(pname):
	df = get_all_skater_fps()
	player = df[df['Player'] == pname]
	return player

def get_goalie_fps(pname):
	df = get_all_goalie_fps()
	player = df[df['Player'] == pname]
	return player

def build_fp_table(players, fps, fps_g):
	df = pd.DataFrame()
	df['Player'] = players
	df['FP'] = fps.apply(lambda x: '{0:.3f}'.format(x))
	df['FP/G'] = fps_g.apply(lambda x: '{0:.3f}'.format(x))
	return df


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("ptype", help="type of player (skater or goalie)")
	args = parser.parse_args()

	data = []

	if args.ptype == 'skater':
		data = get_all_skater_fps()
	elif args.ptype == 'goalie':
		data = get_all_goalie_fps()
	else:
		exit(1)

	print(json.dumps(data))
	sys.stdout.flush()

if __name__ == '__main__':
	main()