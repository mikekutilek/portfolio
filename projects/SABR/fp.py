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
	#batting and fielding data
	players = batters['Name'].astype('str')
	games = batters['G'].astype('float64')
	r = batters['R'].astype('float64')
	
	double = batters['2B'].astype('float64')
	triple = batters['3B'].astype('float64')
	homer = batters['HR'].astype('float64')
	single = batters['H'].astype('float64') - double - triple - homer
	rbi = batters['RBI'].astype('float64')
	sb = batters['SB'].astype('float64')
	cs = batters['CS'].astype('float64')
	bb = batters['BB'].astype('float64') + batters['IBB'].astype('float64')
	hbp = batters['HBP'].astype('float64')
	so = batters['SO'].astype('float64')

	fielder_name = std_fielding_data['Name']
	e = std_fielding_data['E']
	a = std_fielding_data['A']
	pos = std_fielding_data['Pos']

	fps = r + single + (double * 2) + (triple * 3) + (homer * 4) + rbi + (sb * 1.75) - (cs * 0.5) + (bb * 0.75) + (hbp * 0.5) - (so * .1) - e2 + (ofa * 1.05) + (ifa * 0.05)
	fps_g = fps / games

	df = build_fp_table(players, fps, fps_g)

	return df

def get_all_pitcher_fps():
	df = pd.DataFrame()
	page = br.get_standard_pitching_page()
	#table = page.find('table')
	#print(table)
	pitchers = br.get_player_table(page)
	
	#print(pitchers)

	relief_page = br.get_relief_page()
	relievers = br.get_player_table(relief_page)

	qs_page = br.get_starting_page()
	qs_table = br.get_player_table(qs_page)

	players = pitchers['Name'].astype('str')
	games = pitchers['G'].astype('float64')
	ip = pitchers['IP'].astype('float64')
	w = pitchers['W'].astype('float64')
	l = pitchers['L'].astype('float64')
	cg = pitchers['CG'].astype('float64')
	sv = pitchers['SV'].astype('float64')
	h = pitchers['H'].astype('float64')
	er = pitchers['ER'].astype('float64')
	walks = pitchers['BB'].astype('float64')
	ibb = pitchers['IBB'].astype('float64')
	hb = pitchers['HBP'].astype('float64')
	k = pitchers['SO'].astype('float64')

	df2 = pd.merge(pitchers, relievers[['Hold', 'BSv', 'Name']], on=['Name'], how='left').fillna(0)
	print(df2['BSv'])

	#print(df.sort_values(by=['W']))
	#print(qs_table)
	

	hld = relievers['Hold'].astype('float64')
	bsv = relievers['BSv'].astype('float64')

	#now we handle pitcher data
	half_ip = []
	inns = []
	for i in ip:
		inn = int(i)
		half_i = str(i)[-1]
		inns.append(inn)
		half_ip.append(float(half_i))

	innings = pd.Series(inns)
	rem = pd.Series(half_ip)

	

	qs = qs_table['QS'].astype('float64')

	fps = (innings * 1.0) + (rem * 0.33) + (w * 9) - (l * 6) + (cg * 7) + (sv * 8) - (h * 0.25) - er - (walks * 0.5) - (ibb * 0.5) + k + (hld * 7.5) - (bsv * 3)
	fps_g = fps / games

	#df = build_fp_table(players, fps, fps_g)

	return pitchers

def build_fp_table(players, fps, fps_g):
	df = pd.DataFrame()
	df['Player'] = players
	df['FP'] = fps.apply(lambda x: '{0:.2f}'.format(x)).astype('float64')
	df['FP/G'] = fps_g.apply(lambda x: '{0:.2f}'.format(x)).astype('float64')
	return df


print(get_all_pitcher_fps())
"""
#handle batting/fielding data first
ofers = std_fielding_data.loc[std_fielding_data['Pos'].isin(['LF','CF','RF'])]
ifers = std_fielding_data.loc[std_fielding_data['Pos'].isin(['C','1B','2B','SS','3B'])]
e = std_fielding_data.loc[std_fielding_data['Pos'].isin(['C','1B','2B','SS','3B','LF','CF','RF'])]

ofers['Total'] = ofers.groupby(['Name'])['A'].transform('sum')
ifers['Total'] = ifers.groupby(['Name'])['A'].transform('sum')
e['Total'] = e.groupby(['Name'])['E'].transform('sum')

ofers_min = ofers.drop_duplicates(['Name'], keep='first')
ifers_min = ifers.drop_duplicates(['Name'], keep='first')
e_min = e.drop_duplicates(['Name'], keep='first')

df_with_ofa = std_batting_data.merge(ofers_min, on='Name', how='left').fillna(0)
df_with_ifa = std_batting_data.merge(ifers_min, on='Name', how='left').fillna(0)
df_with_e = std_batting_data.merge(e_min, on='Name', how='left').fillna(0)

ofa = df_with_ofa['Total']
ifa = df_with_ifa['Total']
e2 = df_with_e['Total']


page = br.get_team_sp_page()
#table = soup.select_one("table#players_starter_pitching")
tables = soup.findAll("table")
for table in tables:
	rows = table.find_all('tr')
	qs_list = []

	#for table in tables:
	#rows = table.find_all('tr')
	for row in rows:
		#print(row.text.strip())
		cells = row.findAll('td')
		for cell in cells:
			qs_list.append(cell.text.strip())
print(qs_list)
"""