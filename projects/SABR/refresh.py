import numpy as np
import pandas as pd
import fp
import sys, json, argparse
import pymongo #pymongo-3.7.2

def conn():
	return pymongo.MongoClient("mongodb+srv://admin:pdometer@mongo-uwij2.mongodb.net/test?retryWrites=true")

def refresh_table(table_name, df):
	data_json = df.to_json(orient='records')
	client = conn()
	db = client['SABR']
	table = db[table_name]
	table.drop()
	table.insert(json.loads(data_json))

def load_batter_fp():
	df = fp.get_all_batter_fps()
	refresh_table('batter_fp', df)

def load_pitcher_fp():
	df = fp.get_all_pitcher_fps()
	refresh_table('pitcher_fp', df)

def main():
	load_batter_fp()
	load_pitcher_fp()

if __name__ == '__main__':
	main()