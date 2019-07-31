import numpy as np
import pandas as pd
from bs4 import BeautifulSoup, Comment
import requests
import re

def get_page(url):
	r = requests.get(url)
	html = r.text.replace('<!--', '').replace('-->', '')
	return BeautifulSoup(html, "lxml")

def get_table_by_class(page, _class):
	return page.find_all('table',{'class':_class})

def get_table_by_id(page, table_id):
	return page.find_all('table', id=table_id)

def build_df(table, table_index, strings, ints):
	thead = table[table_index].find('thead')
	ths = thead.find_all('th')
	headings = []
	for th in ths:
		headings.append(th.text.strip())
	tbody = table[table_index].find('tbody')
	rows = tbody.find_all('tr')
	data = []
	for row in rows:
		if row.get('class') is not None:
			if 'partial_table' in row.get('class') or row.get('class') == ['thead']:
				continue
		cells = row.find_all(['th', 'td'])
		cells = [cell.text.replace('*', '').replace('#', '').replace('%', '').strip() for cell in cells]
		if cells[1] == 'LgAvg per 600 PA':
			continue
		data.append([cell for cell in cells])
	df = pd.DataFrame(data=data, columns=headings)
	for heading in headings:
		if heading in strings: #Strings
			continue
		elif heading in ints: #Ints
			df[heading] = df[heading].replace('', 0).astype(int)
		else:
			df[heading] = df[heading].replace('', 0).astype('float64')
	
	return df