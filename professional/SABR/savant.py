import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sys
import datetime as dt
import argparse

team_key = {'Orioles': 'BAL', 'Red Sox': 'BOS', 'Yankees': 'NYY', 'Rays': 'TB', 'Blue Jays': 'TOR', 
'Indians': 'CLE', 'White Sox': 'CWS', 'Tigers': 'DET', 'Royals': 'KC', 'Twins': 'MIN',
'Astros': 'HOU', 'Angels': 'LAA', 'Athletics': 'OAK', 'Mariners': 'SEA', 'Rangers': 'TEX',
'Braves': 'ATL', 'Marlins': 'MIA', 'Mets': 'NYM', 'Phillies': 'PHI', 'Nationals': 'WSH', 
'Cubs': 'CHC', 'Reds': 'CIN', 'Brewers': 'MIL', 'Pirates': 'PIT', 'Cardinals': 'STL', 
'Diamondbacks': 'ARI', 'Rockies': 'COL', 'Dodgers': 'LAD', 'Padres': 'SD', 'Giants': 'SF'}

def get_team(team):
	return team_key[team]

def get_page(batter_stands='', position='', group_by='name', sort_col=''):
	url = '''
	https://baseballsavant.mlb.com/statcast_search?
	hfPT=&
	hfAB=&
	hfBBT=&
	hfPR=&
	hfZ=&
	stadium=&
	hfBBL=&
	hfNewZones=&
	hfGT=R%7C&
	hfC=&
	hfSea=2018%7C&
	hfSit=&
	player_type=pitcher&
	hfOuts=&
	opponent=&
	pitcher_throws=&
	batter_stands={}&
	hfSA=&
	game_date_gt=&
	game_date_lt=&
	hfInfield=&
	team=&
	position={}&
	hfOutfield=&
	hfRO=&
	home_road=&
	hfFlag=&
	hfPull=&
	metric_1=&
	hfInn=&
	min_pitches=0&
	min_results=50&
	group_by={}&
	sort_col={}&
	player_event_sort=h_launch_speed&
	sort_order=desc&
	min_pas=0#results
	'''.replace('\t', '').replace('\n', '').strip().format(batter_stands, position, group_by, sort_col)
	r = requests.get(url)
	return BeautifulSoup(r.content, "html.parser")

def get_table(page):
	table = page.find('table',{'id':'search_results'})
	ths = table.find_all('th')
	headings = []
	for th in ths:
		headings.append(th.text.strip())
	tbody = table.find('tbody')
	rows = tbody.find_all('tr')
	data = []
	for row in rows[::2]:
		cells = row.find_all('td')
		#cells = [cell.text.replace('%', '').strip() for cell in cells]
		data.append([cell.text.strip() for cell in cells])

	df = pd.DataFrame(data=data, columns=headings[:-3])
	return df
