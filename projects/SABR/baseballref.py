import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_team_sp_page(season='2018'):
	url = "https://www.baseball-reference.com/leagues/MLB/{}-starter-pitching.shtml".format(season)
	r = requests.get(url)
	return BeautifulSoup(r.content, "html.parser")

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
	return df.sort_values(by=['RA/G'])

def main():
	page = get_team_sp_page()
	print(get_table(page))

if __name__ == '__main__':
	main()