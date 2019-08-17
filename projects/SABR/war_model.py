import numpy as np
import pandas as pd
import matplotlib.pyplot as plt, mpld3
import matplotlib.gridspec as gridspec
import fangraphs as fg
import baseballref as bref
import pymongo
import datetime

CUR_SEASON = '2019'
season_range = np.arange(1903, int(CUR_SEASON))

def conn():
	return pymongo.MongoClient("mongodb+srv://admin:pdometer@mongo-uwij2.mongodb.net/test?retryWrites=true")

def get_war_rank_data():
	client = conn()
	db = client['MLB_TEAM_HISTORICAL']
	war_ranks = []
	bwar_ranks = []
	pwar_ranks = []
	seasons = []
	for season in season_range:
		if season == 1904 or season == 1994:
			continue
		table = db['fg_dashboard_' + str(season)]
		champ = table.find({'FINISH' : 'CHAMPION'})
		year = champ[0]['Year']
		war_rank = champ[0]['WAR_RANK']
		bwar_rank = champ[0]['B_WAR_RANK']
		pwar_rank = champ[0]['P_WAR_RANK']
		war_ranks.append(war_rank)
		bwar_ranks.append(bwar_rank)
		pwar_ranks.append(pwar_rank)
		seasons.append(year)
	df = pd.DataFrame()
	df['WAR_RANK'] = war_ranks
	df['BWAR_RANK'] = bwar_ranks
	df['PWAR_RANK'] = pwar_ranks
	df['YEAR'] = seasons
	df['YEAR'] = pd.to_datetime(df['YEAR'], format='%Y')
	return df

def plot_histogram(df):
	gs = gridspec.GridSpec(4, 4)
	fig = plt.figure(figsize=(8, 8))
	ax = fig.add_subplot(gs[2:4, 1:3])
	ax2 = fig.add_subplot(gs[:2, :2])
	ax3 = fig.add_subplot(gs[:2, 2:])
	fig.suptitle("A Look At Where WS Champions Rank in fWAR")
	ax.set_title('Cumulative fWAR', fontsize=24)
	ax.set_xlabel('fWAR Rank', fontsize=16)
	ax.set_ylabel('Championships', fontsize=16)
	ax2.set_title('Position Player fWAR', fontsize=24)
	ax2.set_xlabel('fWAR Rank', fontsize=16)
	ax2.set_ylabel('Championships', fontsize=16)
	ax3.set_title('Pitcher fWAR', fontsize=24)
	ax3.set_xlabel('fWAR Rank', fontsize=16)
	ax3.set_ylabel('Championships', fontsize=16)
	ax.hist(df['WAR_RANK'].values, bins=np.arange(1, 30)-0.5)
	ax2.hist(df['BWAR_RANK'].values, bins=np.arange(1, 30)-0.5)
	ax3.hist(df['PWAR_RANK'].values, bins=np.arange(1, 30)-0.5)
	fig.tight_layout()
	mpld3.save_html(fig, 'graphs/war_ranks_hist.html')

def plot_yoy(df):
	fig = plt.figure(figsize=(40, 15))
	ax = fig.add_subplot(221)
	ax.set_xlabel('MLB fWAR Rank')
	ax.set_ylabel('Championships')
	ax.grid(color='lightgray')
	war_ranks = df['WAR_RANK']
	bwar_ranks = df['BWAR_RANK']
	pwar_ranks = df['PWAR_RANK']
	ax.plot(df['YEAR'], war_ranks, 'bo')
	ax.plot(df['YEAR'], bwar_ranks, 'go')
	ax.plot(df['YEAR'], pwar_ranks, 'ro')
	mpld3.save_html(fig, 'graphs/war_ranks_line.html')