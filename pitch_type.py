import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from flask import Flask
import sys

pt_data = pd.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Pitching/2018/Pitch Type Pitching Data.csv')

def get_page(pid):
	pitcher_data = pt_data.loc[pt_data['playerid'] == pid]
	pitcher_data = pitcher_data.fillna(0)
	p_index = pitcher_data.index[0]
	#p_id = pitcher_data['playerid'][p_index]
	url = "https://www.fangraphs.com/statsd.aspx?playerid={}&position=P&gds=&gde=&type=6".format(pid)
	r = requests.get(url)
	return BeautifulSoup(r.content, "html.parser")

def get_table(page):
	table = page.find('table',{'class':'rgMasterTable'})
	ths = table.find_all('th')
	headings = []
	for th in ths:
		headings.append(th.text.strip())
	tbody = table.find('tbody')
	rows = tbody.find_all('tr')
	data = []
	for row in rows[2:]:
		cells = row.find_all('td')
		cells = [cell.text.replace('%', '').strip() for cell in cells]
		data.append([cell for cell in cells])

	df = pd.DataFrame(data=data, columns=headings)
	return df

def calculate_averages(data):
	df = pd.DataFrame(columns=['Fastball Average', 'Breaking Ball Average'])
	fb = data['FB%'].astype('float64').mean()
	print(fb)

def main(argv):
	page = get_page(int(argv[1]))
	df = get_table(page)
	json = df.to_json(orient='records')[1:-1]
	print(json)
	sys.stdout.flush()

if __name__ == "__main__":
	main(sys.argv)