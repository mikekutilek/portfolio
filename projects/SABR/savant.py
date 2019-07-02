import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sys, json, re, time

def get_page(batter_stands='', position='', hfInn='', min_results='', group_by='name', sort_col=''):
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
	hfSea=2019%7C&
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
	hfInn={}&
	min_pitches=0&
	min_results={}&
	group_by={}&
	sort_col={}&
	player_event_sort=h_launch_speed&
	sort_order=desc&
	min_pas=0#results
	'''.replace('\t', '').replace('\n', '').strip().format(batter_stands, position, hfInn, min_results, group_by, sort_col)
	r = requests.get(url)
	return BeautifulSoup(r.content, "html.parser")

def get_exp_stats(ptype='', year='', position='', team='', min_results='25'):
	url = '''
	https://baseballsavant.mlb.com/expected_statistics?
	type={}&
	year={}&
	position={}&
	team={}&
	min={}
	'''.replace('\t', '').replace('\n', '').strip().format(ptype, year, position, team, min_results)
	return url
	#r = requests.get(url)
	#html = r.text.replace('<!--', '').replace('-->', '')
	#return BeautifulSoup(r.content, "html.parser")

def get_table(page):
	table = page.find('table',{'id':'search_results'})
	thead = table.find('thead')
	ths = thead.find_all('th')
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