import numpy as np
import pandas as pd
import fangraphs as fg
import baseballref as bref
import pymongo
import re, json

CUR_SEASON = '2019'
season_range = np.arange(2018, int(CUR_SEASON))

def conn():
	return pymongo.MongoClient("mongodb+srv://admin:pdometer@mongo-uwij2.mongodb.net/test?retryWrites=true")

def get_cumulative_war(season, active_roster='0'):
	batter_page = fg.get_team_stats_page(season=season, active=active_roster)
	batter_table = fg.get_table_by_class(batter_page, 'rgMasterTable')
	batter_df = fg.build_df(batter_table, strings=['Team'])
	pitcher_page = fg.get_team_stats_page(ptype='pit', season=season, active=active_roster)
	pitcher_table = fg.get_table_by_class(pitcher_page, 'rgMasterTable')
	pitcher_df = fg.build_df(pitcher_table, strings=['Team'])
	df = pd.merge(batter_df[['#', 'Team', 'WAR']], pitcher_df[['#', 'Team', 'WAR']], on='Team', how='left')
	df['WAR'] = df['WAR_x'] + df['WAR_y']
	df['Year'] = season
	df['Year'] = df['Year'].astype(int)
	df = df.sort_values(by=['WAR'], ascending=False).reset_index(drop=True)
	df['WAR_RANK'] = df.index + 1
	df = df.rename(columns={"WAR_x": "B_WAR", "WAR_y": "P_WAR", "#_x": "B_WAR_RANK", "#_y": "P_WAR_RANK"})
	df['B_WAR_RANK'] = df['B_WAR_RANK'].astype(int)
	df['P_WAR_RANK'] = df['P_WAR_RANK'].astype(int)
	df['FINISH'] = ''
	df = df[['Team', 'Year', 'B_WAR', 'P_WAR', 'WAR', 'B_WAR_RANK', 'P_WAR_RANK', 'WAR_RANK', 'FINISH']]
	return df

def get_ws_champs():
	page = bref.get_page('https://www.baseball-reference.com/postseason/')
	table = bref.get_table_by_id(page, 'postseason_series')
	df = pd.DataFrame(columns=['Year', 'Team'])
	years = []
	champs = []
	rows = table[0].find_all('tr')
	for row in rows:
		cells = row.find_all(['th', 'td'])
		cells = [cell.text.replace('*', '').strip().lower() for cell in cells]
		if "world series" in cells[0]:
			years.append(cells[0].split()[0])
			champs.append(cells[2][:cells[2].index("(")])
	df['Year'] = years
	df['Year'] = df['Year'].astype(int)
	df['Team'] = champs
	return df[df['Year'] >= 1903]

def get_ws_champ(season):
	df = teamname_to_abbr(get_ws_champs(), 'sa')
	return df[df['Year'] == season]

def teamname_to_abbr(df, abbr_type):
	"""
	This method takes a dataframe of players and matches each player's team name against a given Team Abbreviation Type stored in MongoDB
	"""
	client = conn()
	db = client['SABR']
	table = db['teams']
	abbr_df = pd.DataFrame()
	abbr_df['Team'] = df['Team']
	abbr_df['Year'] = df['Year']
	#print(abbr_df)
	team_abbrs = []
	for index, row in abbr_df.iterrows():
		current_season = row['Year']
		full_name = row['Team'].title().strip()
		#full_name = full_name.replace("'", "")
		#print(full_name)

		if 'senators' in full_name.lower():
			if current_season > 1901 and current_season <= 1960:
				team_abbr = 'MIN'
			else:
				team_abbr = 'TEX'
		elif full_name.lower() in ['chi-feds', 'buffeds', 'whales', 'terrapins', 'tip-tops', 'blues', 'whalers', 'green sox', 'blue sox', 'hoosiers', 'packers', 'pepper', 'rebels', 'terriers']:
			team_abbr = full_name
		elif 'colt' in full_name.lower():
			team_abbr = 'HOU'
		else:
			abbr = table.find({"$or":[{'team' : full_name}, {'full_name' : full_name}] })
			team_abbr = abbr[0]['abbrs'][0][abbr_type]
		team_abbrs.append(team_abbr)
	for i in range(len(team_abbrs)):
		df.loc[i, 'Team'] = team_abbrs[i]
	return df

def get_finished_df(season):
	war_df = get_cumulative_war(str(season))
	df = teamname_to_abbr(war_df, 'sa')
	if season < int(CUR_SEASON):
		if season != 1904 and season != 1994:
			champ_row = df['Team'] == get_ws_champ(season)['Team'].values[0]
			idx = df.index[champ_row].tolist()[0]
			df.loc[idx, 'FINISH'] = 'CHAMPION'
	return df

#print(get_finished_df(1962))