import numpy as np
import pandas as pd
import hockeyref as hr

def get_skater_fps(pname):
	skater_page = hr.get_all_skaters_page()
	skaters = hr.get_table(skater_page)
	player = skaters[skaters['Player'] == pname]
	return player['PTS']

def get_goalie_fps(pname):
	goalie_page = hr.get_all_goalies_page()
	goalies = hr.get_table(goalie_page)
	player = goalies[goalies['Player'] == pname]

def build_fp_table()

print(get_skater_fps("Sidney Crosby"))