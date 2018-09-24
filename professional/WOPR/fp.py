import numpy as np
import pandas as pd
import airyards as ay
import wopr

def get_fp():
	f_page = ay.get_pfr_fantasy()
	f_df = ay.get_table(f_page)
	f_df = f_df.replace('', 0)
	s_page = ay.get_pfr_scoring()
	s_df = ay.get_table(s_page)
	s_df = s_df.replace('', 0)
	r_page = ay.get_pfr_rushing()
	r_df = ay.get_table(r_page)
	r_df = r_df.replace('', 0)

	wo_df = wopr.get_wo()
	wopr_df = wopr.get_leaderboards('WR')
	wopr_df.index.names = ['Player', 'Pos']
	#print(wopr_df)

	df2 = pd.merge(f_df,r_df[['Fmb', 'Player']],on='Player', how='left')
	df3 = pd.merge(df2,s_df[['AllTD', 'Player']],on='Player', how='left').fillna(0)
	df4 = pd.merge(df3,wo_df[['WO', 'WO/G', 'Player']],on='Player', how='left').fillna(0)
	#df5 = pd.merge(df4,wopr_df[['wopr']],left_index=True, right_on='Player', how='left').fillna(0)

	passyds = df3['PassYds'].astype('float64')
	passtds = df3['PassTD'].astype('float64')
	ints = df3['Int'].astype('float64')
	rushyds = df3['RushYds'].astype('float64')
	receptions = df3['Rec'].astype('float64')
	recyds = df3['RecYds'].astype('float64')
	tds = df3['AllTD'].astype('float64')
	twoptmd = df3['2PM'].astype('float64')
	twoptcp = df3['2PP'].astype('float64')
	fumbles = df3['Fmb'].astype('float64')
	games = df3['G'].astype('float64')

	fp = (passyds / 30.0) + (passtds * 4.0) - (ints * 2.0) + (rushyds / 10.0) + (receptions * 0.5) + (recyds / 10.0) + (tds * 6.0) + (twoptmd * 2.0) + (twoptcp * 2.0) - (fumbles * 2.0)

	df = pd.DataFrame()
	df['Player'] = f_df['Player']
	df['Pos'] = df4['FantPos']
	df['FP'] = fp.round(2)
	df['WO'] = df4['WO']
	df['FP/G'] = (fp / games).round(2)
	df['WO/G'] = df4['WO/G']
	return df[df['Pos'] == 'RB'].sort_values(by=['WO/G'], ascending=False)

def main():
	print(get_fp())

if __name__ == '__main__':
	main()