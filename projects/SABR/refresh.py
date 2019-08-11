import numpy as np
import pandas as pd
import baseballref as bref
import savant as sa
import fangraphs as fg
import fp
import opener as op
import historical as hist
import json
import pymongo #pymongo-3.7.2
import os
import argparse

CUR_SEASON = "2019"
HIST_SEASON_RANGE = np.arange(1990, 2020)

def conn():
	return pymongo.MongoClient("mongodb+srv://admin:pdometer@mongo-uwij2.mongodb.net/test?retryWrites=true")

def refresh_table(db_name, table_name, df):
	data_json = df.to_json(orient='records')
	client = conn()
	db = client[db_name]
	table = db[table_name]
	table.drop()
	table.insert(json.loads(data_json))

def insert_to_table(db_name, table_name, df):
	data_json = df.to_json(orient='records')
	client = conn()
	db = client[db_name]
	table = db[table_name]
	table.insert(json.loads(data_json))

def load_teams():
	df = json.load(open("data/teams.json"))
	client = conn()
	db = client['SABR']
	table = db['teams']
	table.drop()
	table.insert(df)

def load_team_historical():
	for season in HIST_SEASON_RANGE:
		df = hist.get_finished_df(season)
		refresh_table('MLB_TEAM_HISTORICAL', 'fg_dashboard_'+str(season), df)

def load_bref_team_sp():
	url = "https://www.baseball-reference.com/leagues/MLB/{}-starter-pitching.shtml".format(CUR_SEASON)
	page = bref.get_page(url)
	df = bref.build_df(bref.get_table_by_class(page, 'stats_table'), 0, ['Tm'], ['']).sort_values(by=['RA/G'])
	refresh_table('SABR', 'bref_team_sp', df)

def load_batter_fp():
	df = fp.get_all_batter_fps()
	refresh_table('SABR', 'batter_fp', df)

def load_pitcher_fp():
	df = fp.get_all_pitcher_fps()
	refresh_table('SABR', 'pitcher_fp', df)

def load_opener_candidates():
	rrp_df = op.get_all_candidates('R', 'RP')
	lrp_df = op.get_all_candidates('L', 'RP')
	rsp_df = op.get_all_candidates('R', 'SP')
	lsp_df = op.get_all_candidates('L', 'SP')
	refresh_table('SABR', 'opener_candidates', rrp_df)
	insert_to_table('SABR', 'opener_candidates', lrp_df)
	insert_to_table('SABR', 'opener_candidates', rsp_df)
	insert_to_table('SABR', 'opener_candidates', lsp_df)

def main():
	parser = argparse.ArgumentParser(description='SABR Daily Data Refresh')
	parser.add_argument('--hist', action='store_true', help="Choose whether to run the historical data refresh or not")
	args = parser.parse_args()

	if args.hist:
		print("### RUNNING HISTORICAL LOAD ###")
		load_teams()
		load_team_historical()
		print("### HISTORICAL LOAD COMPLETES ###")
	print("### RUNNING DAILY LOAD ###")
	load_bref_team_sp()
	load_batter_fp()
	load_pitcher_fp()
	load_opener_candidates()
	print("### DAILY LOAD COMPLETES ###")

if __name__ == '__main__':
	main()