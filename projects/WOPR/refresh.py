import numpy as np
import pandas as pd
import airyards as ay
import sys, json, argparse
import pymongo #pymongo-3.7.2

def conn():
	return pymongo.MongoClient("mongodb+srv://admin:pdometer@mongo-uwij2.mongodb.net/test?retryWrites=true")

def load_air_yards():
	df = ay.get_ay_data()
	data_json = df.to_json(orient='records')
	client = conn()
	db = client['WOPR']
	table = db.air_yards
	table.drop()
	table.insert(json.loads(data_json))

def load_pfr_rushing():
	page = ay.get_pfr_rushing()
	df = ay.get_table(page)
	data_json = df.to_json(orient='records')
	client = conn()
	db = client['WOPR']
	table = db.pfr_rushing
	table.drop()
	table.insert(json.loads(data_json))

def load_pfr_fantasy():
	page = ay.get_pfr_fantasy()
	df = ay.get_table(page)
	data_json = df.to_json(orient='records')
	client = conn()
	db = client['WOPR']
	table = db.pfr_fantasy
	table.drop()
	table.insert(json.loads(data_json))

def load_pfr_scoring():
	page = ay.get_pfr_scoring()
	df = ay.get_table(page)
	data_json = df.to_json(orient='records')
	client = conn()
	db = client['WOPR']
	table = db.pfr_scoring
	table.drop()
	table.insert(json.loads(data_json))

def main():
	load_air_yards()
	load_pfr_rushing()
	load_pfr_fantasy()
	load_pfr_scoring()

if __name__ == '__main__':
	main()