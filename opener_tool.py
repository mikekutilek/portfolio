import numpy
import pandas
import requests
from functools import reduce
import sys

#first_inning_pitching_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Pitching/2018/1st Inning Pitching Data.csv')
#rest_of_game_pitching_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Pitching/2018/Rest of Game Pitching Data.csv')

first_time_pitching_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Pitching/2018/1st Time Through Pitching Data.csv')
second_time_pitching_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Pitching/2018/2nd Time Through Pitching Data.csv')
third_time_pitching_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Pitching/2018/3rd Time Through Pitching Data.csv')

def replace_percents(data):
	strings = data.select_dtypes(['object'])
	data[strings.columns] = strings.apply(lambda x: x.str.replace('%', ''))

def calc_hardhit_diff():
	replace_percents(first_inning_pitching_data)
	replace_percents(rest_of_game_pitching_data)
	pitcher_data = first_inning_pitching_data.loc[first_inning_pitching_data['IP'] >= 5]
	hard_first = pitcher_data['Hard%']
	pitcher_data = rest_of_game_pitching_data.loc[rest_of_game_pitching_data['IP'] >= 15]
	hard_rest = pitcher_data['Hard%']

	hard_first_data = pandas.DataFrame()
	hard_first_data['Name'] = first_inning_pitching_data['Name']
	hard_first_data['Hard% (1st Inning)'] = hard_first.astype(float).multiply(100)
	hard_rest_data = pandas.DataFrame()
	hard_rest_data['Name'] = rest_of_game_pitching_data['Name']
	hard_rest_data['Hard% (Rest of Game)'] = hard_rest.astype(float).multiply(100)

	diff_data = hard_first_data.merge(hard_rest_data, on='Name', how='left').fillna(0)
	diff_data['Difference'] = diff_data['Hard% (1st Inning)'] - diff_data['Hard% (Rest of Game)']
	print(diff_data.sort_values(by='Difference', ascending=False))

def calc_FIP_diff(data1, data2):
	replace_percents(data1)
	replace_percents(data2)
	pitcher_data = data1.loc[data1['IP'] >= 5]
	xFIP_first = pitcher_data['FIP']
	pitcher_data = data2.loc[data2['IP'] >= 15]
	xFIP_rest = pitcher_data['FIP']

	xFIP_first_data = pandas.DataFrame()
	xFIP_first_data['Name'] = data1['Name']
	xFIP_first_data['FIP (1st Inning)'] = round(xFIP_first.astype(float), 2)
	xFIP_rest_data = pandas.DataFrame()
	xFIP_rest_data['Name'] = data2['Name']
	xFIP_rest_data['FIP (Rest of Game)'] = round(xFIP_rest.astype(float), 2)

	diff_data = xFIP_first_data.merge(xFIP_rest_data, on='Name', how='left').fillna(0)
	diff_data['Difference'] = diff_data['FIP (1st Inning)'] - diff_data['FIP (Rest of Game)']
	print(diff_data.sort_values(by='Difference', ascending=False))
	diff_data.to_csv('c:/Users/mkutilek/Documents/Data/Fangraphs/Pitching/2018/FIP 1st to Rest Inning Difference Pitching Data.csv')

def calc_xFIP_diff(data1, data2):
	replace_percents(data1)
	replace_percents(data2)
	pitcher_data = data1.loc[data1['IP'] >= 5]
	xFIP_first = pitcher_data['x FIP']
	pitcher_data = data2.loc[data2['IP'] >= 15]
	xFIP_rest = pitcher_data['x FIP']

	xFIP_first_data = pandas.DataFrame()
	xFIP_first_data['Name'] = data1['Name']
	xFIP_first_data['xFIP (1st Inning)'] = round(xFIP_first.astype(float), 2)
	xFIP_rest_data = pandas.DataFrame()
	xFIP_rest_data['Name'] = data2['Name']
	xFIP_rest_data['xFIP (Rest of Game)'] = round(xFIP_rest.astype(float), 2)

	diff_data = xFIP_first_data.merge(xFIP_rest_data, on='Name', how='left').fillna(0)
	diff_data['Difference'] = diff_data['xFIP (1st Inning)'] - diff_data['xFIP (Rest of Game)']
	print(diff_data.sort_values(by='Difference', ascending=False))
	diff_data.to_csv('c:/Users/mkutilek/Documents/Data/Fangraphs/Pitching/2018/xFIP 1st to Rest Inning Difference Pitching Data.csv')

def calc_wOBA_orders(data1, data2, data3):
	pitcher_data = data1.loc[data1['IP'] >= 5]
	wOBA_first = pitcher_data['w OBA']
	pitcher_data = data2.loc[data2['IP'] >= 5]
	wOBA_second = pitcher_data['w OBA']
	pitcher_data = data3.loc[data3['IP'] >= 5]
	wOBA_third = pitcher_data['w OBA']

	wOBA_first_data = pandas.DataFrame()
	wOBA_first_data['Name'] = data1['Name']
	wOBA_first_data['Team'] = data1['Team']
	wOBA_first_data['wOBA (1st Time Through)'] = wOBA_first.astype(float)

	wOBA_second_data = pandas.DataFrame()
	wOBA_second_data['Name'] = data2['Name']
	wOBA_second_data['Team'] = data2['Team']
	wOBA_second_data['wOBA (2nd Time Through)'] = wOBA_second.astype(float)

	wOBA_third_data = pandas.DataFrame()
	wOBA_third_data['Name'] = data3['Name']
	wOBA_third_data['Team'] = data3['Team']
	wOBA_third_data['wOBA (3rd Time Through)'] = wOBA_third.astype(float)

	dfs = [wOBA_first_data, wOBA_second_data, wOBA_third_data]
	wOBA_data = reduce(lambda left,right: pandas.merge(left,right,on='Name'), dfs)
	#wOBA_data = wOBA_first_data.merge(wOBA_second_data, on='Name', how='left').merge(wOBA_third_data, on='Name', how='left')
	return wOBA_data

def calc_wOBA_slash(pitcher, wOBA_data):
	#wOBA_data = calc_wOBA_orders(first_time_pitching_data, second_time_pitching_data, third_time_pitching_data)
	pitcher_data = wOBA_data.loc[wOBA_data['Name'] == pitcher]
	first = str(format(pitcher_data.iloc[0]['wOBA (1st Time Through)'], '.3f'))[1:]
	second = str(format(pitcher_data.iloc[0]['wOBA (2nd Time Through)'], '.3f'))[1:]
	third = str(format(pitcher_data.iloc[0]['wOBA (3rd Time Through)'], '.3f'))[1:]
	print(pitcher + ": " + first + "/" + second + "/" + third)
#calc_hardhit_diff()
#calc_xFIP_diff(first_inning_pitching_data, rest_of_game_pitching_data)

def calc_team_OBA_slash(team):
	wOBA_data = calc_wOBA_orders(first_time_pitching_data, second_time_pitching_data, third_time_pitching_data)
	team_data = wOBA_data.loc[wOBA_data['Team'] == team]
	print("\n" + team + " pitchers wOBA slash lines")
	for index, pitcher in team_data.iterrows():
		calc_wOBA_slash(pitcher['Name'], team_data)



def main():
	data = {'name': 'Mike Kutilek'}
	print(data)
	sys.stdout.flush()

if __name__ == '__main__':
	main()