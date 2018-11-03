import pandas as pd
import math
from datetime import datetime
from itertools import product
import matplotlib.pyplot as plt
#import numpy as np from scipy import stats
#pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
plt.rcParams['figure.figsize'] = (15, 5)

# read zone lookup table
zones = 'taxi_zone_lookup.csv'
zonesLookup = pd.read_csv(zones)

# read taxi data for Jan 2018
data='D:\Masters\ADM_HW2\yellow_tripdata_2018-01.csv'
yt_data = pd.read_csv(data)
yt_data=yt_data[yt_data['tpep_dropoff_datetime']>='2018']
yt_data=yt_data[yt_data['trip_distance']>0.0]
rq1_data= yt_data.merge(zonesLookup[['LocationID','Borough']],how='inner', left_on='PULocationID', right_on='LocationID')
rq1_data=rq1_data[rq1_data['tpep_pickup_datetime']<rq1_data['tpep_dropoff_datetime']]

#1.1
rq1_data['price_per_mile']=(rq1_data.total_amount/rq1_data.trip_distance)

#1.2
mean_1=rq1_data.groupby('Borough')['price_per_mile'].mean()
std_1=rq1_data.groupby('Borough')['price_per_mile'].std()
mean_1
std_1
mean_1.plot(kind='line')
std_1.plot(kind='line')


#1.3
#creating combination of Borough in the data set
listBorough=rq1_data.groupby('Borough')["Borough"].first()
combinationBorough= list(product(listBorough,listBorough))
resultDF=pd.DataFrame(combinationBorough,columns=["Borough 1","Borough 2"])
#function to calculate T-Test with two following groups
def calculateTTest(vectorA,vectorB):
    t=(vectorA.mean()-vectorB.mean())/math.sqrt((vectorA.var()/len(vectorA))+(vectorB.var()/len(vectorB)))
    return t

#calculating T-Test for every combination
res=[]
for index, row in resultDF.iterrows():
   res.append(calculateTTest(rq1_data[rq1_data['Borough']==row['Borough 1']]['price_per_mile'], rq1_data[rq1_data['Borough']==row['Borough 2']]['price_per_mile']))

resultDF["T-Test"]=res
result

#from the results we can observe that the price rate between multiple boroughs in different. Unkown borough has much more difference with other boroughs
# Highest difference is with the Queens and unknown following with the difference of Manhattan and Unknown and Brooklyn and Unknown

#2.1
#calculating time in seconds for weighted price per mile
rq1_data['tpep_pickup_datetime'] =  pd.to_datetime(rq1_data['tpep_pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
rq1_data['tpep_dropoff_datetime'] =  pd.to_datetime(rq1_data['tpep_dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')
rq1_data['weighted_price_per_mile']=rq1_data['price_per_mile']/(rq1_data['tpep_dropoff_datetime']-rq1_data['tpep_pickup_datetime']).astype('timedelta64[s]')

#2.2
#calculating mean and standard deviation of weighted price per mile

mean_2=rq1_data.groupby('Borough')['weighted_price_per_mile'].mean()
std_2=rq1_data.groupby('Borough')['weighted_price_per_mile'].std()
mean_2
std_2
mean_2.plot(kind='line')
std_2.plot(kind='line')

#by looking at the plots of mean and standard deviation.
#we see that EWR borough has the heightest mean and standard deviation among the other boroughs

res=[]
for index, row in resultDF.iterrows():
   res.append(calculateTTest(rq1_data[rq1_data['Borough']==row['Borough 1']]['weighted_price_per_mile'], rq1_data[rq1_data['Borough']==row['Borough 2']]['weighted_price_per_mile']))

resultDF["T-Test Weighed"]=res
resultDF
#We have observed that by using weighted price per mile we have generally reduced the difference between boroughs
#Few boroughs have increased the difference in weighted price per mile like Unknown and Staten Island, QUeens and Manhattan
