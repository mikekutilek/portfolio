import numpy as np
import pandas as pd
import requests

def get_ay_data():
	url = "http://airyards.com/2018/weeks"
	r = requests.get(url)
	df = pd.DataFrame(r.json())
	return df

def main():
	print(get_ay_data())

if __name__ == '__main__':
	main()