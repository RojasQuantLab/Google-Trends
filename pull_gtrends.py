import pytrends
import time
from pytrends.request import TrendReq
from random import randint
import pandas as pd


pytrend = TrendReq(hl='en-US', tz=360)
#Search terms (taken from Preis, et. al, 2013): 
terms = ["debt", "color", "stocks", "restaurant", "portfolio", "inflation", 
         "housing", "dow jones", "revenue", "economics", "credit", "markets", 
         "return", "unemployment", "money", "religion", "cancer", "growth", 
         "investment", "hedge", "marriage", "bonds", "derivatives", "headlines", 
         "profit" , "society", "leverage", "loss", "cash", "office", "fine", "stock market", 
         "banking", "crisis", "happy", "car", "nasdaq", "gains", "finance", "sell", "invest", 
         "fed", "house", "metals", "travel", "returns", "gain", "default", "present", "holiday", 
         "water", "rich", "risk", "gold", "success", "oil", "war", "economy", "chance", 
         "short selling", "lifestyle", "earnings", "arts", "culture", "bubble", "buy", "trader", 
         "tourism", "politics", "energy", "consume", "consumption", "freedom", 
         "dividend", "world", "conflict", "kitchen", "forex", "home", "crash", "transaction", 
         "garden", "fond", "train", "labor", "fun", "environment", "ring"]

#Set up time frames
timeframes = []
datelist = pd.date_range('2004-01-01', '2018-01-01', freq="AS")
date = datelist[0]
while date <= datelist[len(datelist)-1]:
	start_date = date.strftime("%Y-%m-%d")
	end_date = (date+4).strftime("%Y-%m-%d")
	timeframes.append(start_date+' '+end_date)
	date = date+3

data_all = pd.DataFrame()
#4 years maximum for weekly data: 
for term in terms:
	kw_list = [term, 'google']
	start_date = "2004-01-01"
	end_date = "2008-01-01"
	results = pd.DataFrame()
	count = 1
	while count < 5: 
		timeframe = start_date + " " + end_date
		pytrend.build_payload(kw_list, cat=0, timeframe = timeframe)
		df=pytrend.interest_over_time()
		df = df.drop(['isPartial', 'google'], axis=1)
		if count != 1: 
			if df[term].values[0]==0:
				scaling_factor = 1
			else: 
				#Scaling factor:
				scaling_factor = float(results[term].values[-1])/float(df[term].values[0]) 
				#print "Scaling Factor: "+str(scaling_factor)
			df = df*scaling_factor
			results=results.append(df[1:])
		else: 
			results = results.append(df)
		start_date = df.index[-1].strftime("%Y-%m-%d")
		end_date = "20" + str(int(start_date[2:4])+4) + "-" + start_date[5:]
		count = count+1 
	if kw_list != [terms[0]]:
		data_all = pd.concat([data_all, results], axis=1)
	print term

#Export as .csv file
data_all.to_csv('gtrends_results.csv')