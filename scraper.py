import bs4 as bs
import requests
import scraperwiki
import pandas as pd
import re
import json
from time import sleep

def scrape_wiki_table(url):

	year = url[-4:]

	r = requests.get(url)

	r_content = r.content

	soup = bs.BeautifulSoup(r_content, 'lxml')

	tables = soup.find_all("table")

	for table in tables:
		th = table.find('th')
		count_th = len(table.find_all('th'))
		if th is None:
			pass
		else:
			th_text = th.text
#			print(str(table))
#			print(th_text)
			if count_th >= 7 and th_text.startswith("Entered"):			#REQUIRED TO GET RIGHT TABLE
				df = pd.read_html(str(table))[0]
				df.columns = ['date_entered','weeks_in_top_10','single','artist','peak','date_peak_reached','weeks_at_peak']

				#DATA CLEANING
				df['single'] = df['single'].apply(lambda x:str(x).replace('"',''))
				df['single'] = df['single'].apply(lambda x:str(x).replace(' ‡',''))
				df['single'] = df['single'].apply(lambda x:str(x).replace(' ♦',''))
				df['single'] = df['single'].apply(lambda x: re.sub(' \[.*\]', '', str(x)))

				filter_year = df['date_entered'].str.contains(year)
				df = df[filter_year]

				filter_text = df['date_entered'].str.contains('Singles')
				df = df[~filter_text]

				for tuple in df.itertuples():
					data = {}
					data.update([ ('id', str(year) + str(getattr(tuple, "Index"))), ('year', year), ('entered_week_ending', getattr(tuple, "date_entered")), ('weeks_in_top_10', getattr(tuple, 'weeks_in_top_10')), ('single_title', getattr(tuple, 'single')), ('artist', getattr(tuple, 'artist')), ('peak', getattr(tuple, 'peak')), ('peak_reached_week_ending', getattr(tuple, 'date_peak_reached')), ('weeks_at_peak', getattr(tuple, 'weeks_at_peak'))])
					scraperwiki.sqlite.save(unique_keys = ['id'], data = data, table_name="swdata")

				print("Year: " + str(year))
				sw_query = "* FROM swdata WHERE entered_week_ending GLOB '*" + str(year) + "' LIMIT 5"
				print(scraperwiki.sql.select(sw_query))

def scrape_all_lists():
	with open('wiki-lists.json') as json_file:  
		data = json.load(json_file)
		for item in data:		
			item["listLabel"] = item["listLabel"].replace(' ','_')
			url = 'https://en.wikipedia.org/wiki/' + item["listLabel"]
			print(url)
			scrape_wiki_table(url)
			sleep(1)

scrape_all_lists()
#scrape_wiki_table('https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_1991')