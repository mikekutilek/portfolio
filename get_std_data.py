import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from flask import Flask
import sys
import json

pt_data = pd.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Pitching/2018/Pitch Type Pitching Data.csv')

def main():
	df = pd.DataFrame(columns=['Name', 'playerid'])
	df['Name'] = pt_data['Name']
	df = pd.DataFrame(df.Name.str.split(' ',1).tolist(), columns = ['fname','lname'])
	df['Name'] = pt_data['Name']
	df['playerid'] = pt_data['playerid']
	#json = df.to_json(orient='records')[1:-1]
	print(df.sort_values(by=['lname']).to_json(orient='records'))
	sys.stdout.flush()

if __name__ == "__main__":
	main()