import numpy as np
import pandas as pd
import baseballref as bref
import savant as sa
import fangraphs as fg
import fp
import opener as op
import json
import pymongo #pymongo-3.7.2
import os

if 'DYNO' in os.environ:
	chrome_options = Options()
	chrome_options.binary_location = GOOGLE_CHROME_BIN
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--no-sandbox')
	driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

def conn():
	return pymongo.MongoClient("mongodb+srv://admin:pdometer@mongo-uwij2.mongodb.net/test?retryWrites=true")

def refresh_table(table_name, df):
	data_json = df.to_json(orient='records')
	client = conn()
	db = client['SABR']
	table = db[table_name]
	table.drop()
	table.insert(json.loads(data_json))

def insert_to_table(table_name, df):
	data_json = df.to_json(orient='records')
	client = conn()
	db = client['SABR']
	table = db[table_name]
	table.insert(json.loads(data_json))

def load_teams():
	df = json.load(open("data/teams.json"))
	client = conn()
	db = client['SABR']
	table = db['teams']
	table.drop()
	table.insert(df)

def load_bref_team_sp():
	page = bref.get_team_sp_page()
	df = bref.get_table(page)
	refresh_table('bref_team_sp', df)

def load_batter_fp():
	df = fp.get_all_batter_fps()
	refresh_table('batter_fp', df)

def load_pitcher_fp():
	df = fp.get_all_pitcher_fps()
	refresh_table('pitcher_fp', df)

def load_opener_candidates():
	rrp_df = op.get_all_candidates('R', 'RP')
	lrp_df = op.get_all_candidates('L', 'RP')
	rsp_df = op.get_all_candidates('R', 'SP')
	lsp_df = op.get_all_candidates('L', 'SP')
	refresh_table('opener_candidates', rrp_df)
	insert_to_table('opener_candidates', lrp_df)
	insert_to_table('opener_candidates', rsp_df)
	insert_to_table('opener_candidates', lsp_df)

def load_expected_stats():
	url = sa.get_exp_stats()

def main():
	load_bref_team_sp()
	load_batter_fp()
	load_pitcher_fp()
	#load_opener_candidates()
	#load_teams()

if __name__ == '__main__':
	main()