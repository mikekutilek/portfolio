import numpy as np
import pandas as pd
import airyards as ay

def get_leaderboards(position):
	df = ay.get_ay_data()
	totals = df[df['position'] == position].groupby(['full_name', 'position'])['air_yards', 'racr', 'rec', 'rec_yards', 'rush_td', 'rush_yards', 'tar', 'td', 'team_air', 'tm_att', 'wopr', 'yac'].sum()
	averages = df[df['position'] == position].groupby(['full_name', 'position'])['air_yards', 'aypt', 'racr', 'rec', 'rec_yards', 'rush_td', 'rush_yards', 'tar', 'target_share', 'td', 'team_air', 'tm_att', 'wopr', 'yac'].mean().round(2)
	return averages.sort_values(by=['wopr'], ascending=False)

def get_week_by_week(name):
	df = ay.get_ay_data()
	player = df.loc[df['full_name'] == name]
	return player.sort_values(by=['week'])

def get_wo():
	page = ay.get_pfr_rushing()
	df = ay.get_table(page)
	df = df.replace('', 0)
	attempts = df['Att'].astype('float64')
	targets = df['Tgt'].astype('float64')
	games = df['G'].astype('float')
	df['WO'] = (attempts * 0.58) + (targets * 1.19)
	df['WO/G'] = (df['WO'] / games).round(2)
	return df.sort_values(by=['WO/G'], ascending=False)

def main():
	print(get_wo())

if __name__ == '__main__':
	main()