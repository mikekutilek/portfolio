import numpy as np
import pandas as pd
import hockeyref as hr
import sys, json, argparse
import pymongo #pymongo-3.7.2

def conn():
	return pymongo.MongoClient("mongodb+srv://admin:pdometer@mongo-uwij2.mongodb.net/test?retryWrites=true")

def load_skater_basic():
	page = hr.get_all_skaters_page()
	df = hr.get_table(page)
	data_json = df.to_json(orient='records')
	client = conn()
	db = client['Corsica']
	table = db.skater_basic
	table.drop()
	table.insert(json.loads(data_json))

def load_skater_advanced():
	page = hr.get_advanced_skaters_page()
	df = hr.get_table(page)
	data_json = df.to_json(orient='records')
	client = conn()
	db = client['Corsica']
	table = db.skater_advanced
	table.drop()
	table.insert(json.loads(data_json))

def load_goalie_basic():
	page = hr.get_all_goalies_page()
	df = hr.get_table(page)
	data_json = df.to_json(orient='records')
	client = conn()
	db = client['Corsica']
	table = db.goalie_basic
	table.drop()
	table.insert(json.loads(data_json))

def main():
	load_skater_basic()
	load_skater_advanced()
	load_goalie_basic()

if __name__ == '__main__':
	main()