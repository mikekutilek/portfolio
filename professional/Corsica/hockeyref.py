import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_all_skaters_page(season='2018'):
	url = "https://www.hockey-reference.com/leagues/NHL_{}_skaters.html".format(season)
	r = requests.get(url)
	return BeautifulSoup(r.content, "html.parser")

def get_all_goalies_page(season='2018'):
	url = "https://www.hockey-reference.com/leagues/NHL_{}_goalies.html".format(season)
	r = requests.get(url)
	return BeautifulSoup(r.content, "html.parser")

def get_table(page):
	table = page.find('table',{'class':'stats_table'})
	thead = table.find('thead')
	ths = thead.find_all('th')
	headings = []
	for th in ths[16:]:
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

if __name__ == '__main__':
	main()