import numpy as np
import pandas as pd
import fangraphs as fg
import savant as sa
import pymongo #pymongo-3.7.2

def conn():
	return pymongo.MongoClient("mongodb+srv://admin:pdometer@mongo-uwij2.mongodb.net/test?retryWrites=true")

def get_all_pitchers():
	client = conn()
	db = client['SABR']
	table = db['teams']
	"""
	This method takes the full active pitcher list from fangraphs
	"""
	#p1 = fg.get_all_pitchers_page()
	p2 = fg.get_player_stats_page(active='1')
	#df = fg.get_table(p1)
	df = fg.get_table(p2)
	active_df = pd.DataFrame()
	active_df['Name'] = df['Name']
	active_df['Team'] = df['Team']
	#print(active_df)
	active_df['fullname'] = ''
	for index, row in active_df.iterrows():
		#continue;
		#print(row)
		team_abbr = table.find({ "team" : row['Team'] })
		"""
		if row['Team'] != '- - -':
			row['Team'] = sa.get_team(row['Team'])
		elif row['Team'] == '- - -':
			player = active_df.loc[active_df['Name'] == row['Name']]
			row['Team'] = sa.get_team(player['Team'].to_string(index=False))
		else:
			row['Team'] = sa.get_team('NA')
		"""
		#print(row['Name'], row['Team'])
		active_df.loc[index, 'fullname'] = row['Name'].replace(' ', '').strip().lower()
		row['Team'] = team_abbr[0]['abbrs'][0]['sa']
		#print(row['Team'])
	return active_df

print(get_all_pitchers())