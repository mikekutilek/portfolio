import numpy as np
import pandas as pd
from bs4 import BeautifulSoup, Comment
import requests
import re

def get_team_standings_page():
	url = "https://www.baseball-reference.com/leagues/MLB-standings.shtml"
	r = requests.get(url)
	html = r.text.replace('<!--', '').replace('-->', '')
	return BeautifulSoup(html, "lxml")

def get_team_sp_page(season='2018'):
	url = "https://www.baseball-reference.com/leagues/MLB/{}-starter-pitching.shtml".format(season)
	r = requests.get(url)
	return BeautifulSoup(r.content, "html.parser")

def get_standard_pitching_page(season='2018'):
	url = "https://www.baseball-reference.com/leagues/MLB/{}-standard-pitching.shtml".format(season)
	r = requests.get(url)
	html = r.text.replace('<!--', '').replace('-->', '')
	return BeautifulSoup(html, 'lxml')

def get_relief_page(season='2018'):
	url = "https://www.baseball-reference.com/leagues/MLB/{}-reliever-pitching.shtml".format(season)
	r = requests.get(url)
	html = r.text.replace('<!--', '').replace('-->', '')
	return BeautifulSoup(html, 'lxml')

def get_starting_page(season='2018'):
	url = "https://www.baseball-reference.com/leagues/MLB/{}-starter-pitching.shtml".format(season)
	r = requests.get(url)
	html = r.text.replace('<!--', '').replace('-->', '')
	return BeautifulSoup(html, 'lxml')

def get_sb_pitching_page(season='2018'):
	url = "https://www.baseball-reference.com/leagues/MLB/{}-basesituation-pitching.shtml".format(season)
	r = requests.get(url)
	html = r.text.replace('<!--', '').replace('-->', '')
	return BeautifulSoup(html, 'lxml')

def get_std_batting_page(season='2018'):
	url = "https://www.baseball-reference.com/leagues/MLB/{}-standard-batting.shtml".format(season)
	r = requests.get(url)
	html = r.text.replace('<!--', '').replace('-->', '')
	return BeautifulSoup(html, 'lxml')

def get_std_fielding_page(season='2018'):
	url = "https://www.baseball-reference.com/leagues/MLB/{}-standard-fielding.shtml".format(season)
	r = requests.get(url)
	html = r.text.replace('<!--', '').replace('-->', '')
	return BeautifulSoup(html, 'lxml')

def get_of_fielding_page(season='2018'):
	url = "https://www.baseball-reference.com/leagues/MLB/{}-specialpos_of-fielding.shtml".format(season)
	r = requests.get(url)
	html = r.text.replace('<!--', '').replace('-->', '')
	return BeautifulSoup(html, 'lxml')

def get_player_table(page):
	table = page.find_all('table',{'class':'stats_table'})
	thead = table[1].find('thead')

	#trs = thead.find_all('tr')[1]
	ths = thead.find_all('th')
	headings = []
	for th in ths:
		headings.append(th.text.strip())
	tbody = table[1].find('tbody')
	rows = tbody.find_all('tr')
	data = []
	for row in rows:
		#print(type(row.get('class')))
		if 'partial_table' in row.get('class') or row.get('class') == ['thead']:
			#print(row)
			continue
		cells = row.find_all(['th', 'td'])
		#print(type(cells))
		cells = [cell.text.replace('*', '').replace('#', '') for cell in cells]
		#print(type(cells))
		data.append([cell for cell in cells])

	df = pd.DataFrame(data=data, columns=headings)
	return df

def get_table(page):
	table = page.find('table',{'class':'stats_table'})
	thead = table.find('thead')
	#trs = thead.find_all('tr')[1]
	ths = thead.find_all('th')
	headings = []
	for th in ths:
		headings.append(th.text.strip())
	tbody = table.find('tbody')
	rows = tbody.find_all('tr')
	data = []
	for row in rows:
		if row.get('class') == ['partial_table'] or row.get('class') == ['thead']:
			continue
		cells = row.find_all(['th', 'td'])
		cells = [cell.text.replace('%', '').strip() for cell in cells]
		data.append([cell for cell in cells])
	df = pd.DataFrame(data=data, columns=headings)
	for heading in headings:
		if heading in ['Player', 'Tm', 'Pos']: #Strings
			continue
		elif heading in ['Rk', 'Age']: #Ints
			df[heading] = df[heading].replace('', 0).astype(int)
		else:
			#print(heading)
			df[heading] = df[heading].replace('', 0).astype('float64')
	
	return df.sort_values(by=['RA/G'])

def get_table_by_id(page, table_id):
	print(type(table_id))
	print(table_id)
	table = page.find('table', id=table_id)
	thead = table.find('thead')
	#trs = thead.find_all('tr')[1]
	ths = thead.find_all('th')
	headings = []
	for th in ths:
		headings.append(th.text.strip())
	tbody = table.find('tbody')
	rows = tbody.find_all('tr')
	data = []
	for row in rows:
		if row.get('class') == ['partial_table'] or row.get('class') == ['thead']:
			continue
		cells = row.find_all(['th', 'td'])
		cells = [cell.text.replace('%', '').strip() for cell in cells]
		data.append([cell for cell in cells])
	df = pd.DataFrame(data=data, columns=headings)
	return df

def get_teams():
	page = get_team_standings_page()
	table = get_table_by_id(page, 'expanded_standings_overall')
	df = table['Tm']
	return df